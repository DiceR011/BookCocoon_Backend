import httpx
import xml.etree.ElementTree as ET
import re
from api.schemas.book import BookCreate
from fastapi import APIRouter, HTTPException

# FastAPIのインスタンス作成
router = APIRouter()

# 名前空間の設定
namespaces = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "dcndl": "http://ndl.go.jp/dcndl/terms/"
}

@router.get("/library/{isbn}", response_model=BookCreate)
async def get_book_info(isbn: str):
    # URL作成
    url = f"https://ndlsearch.ndl.go.jp/api/opensearch?isbn={isbn}"

    # httpxを使って非同期にリクエストを送る
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
    
    # レスポンスのステータスコードが200でない場合
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="書籍情報の取得に失敗しました")

    # XMLをパース
    root = ET.fromstring(response.text)

    # 必要な情報を取得
    item = root.find(".//item")
    if item is None:
        raise HTTPException(status_code=404, detail="書籍が見つかりません")

    title = item.find("title").text
    isbn_value = item.find(".//dc:identifier[@xsi:type='dcndl:ISBN']", namespaces=namespaces).text
    extent = item.find("dc:extent", namespaces=namespaces).text
    author = item.find("author").text if item.find("author") is not None else "著者情報なし"

    # ページ数を数値部分のみ抽出
    page_count_match = re.search(r'(\d+)', extent)  # 正規表現でページ数の数字を抽出
    page_count = int(page_count_match.group(1)) if page_count_match else None  # 数字部分を整数に変換

    # 結果を返す
    return {
        "title": title,
        "author": author,
        "isbn": isbn_value,
        "total_page": page_count
    }
