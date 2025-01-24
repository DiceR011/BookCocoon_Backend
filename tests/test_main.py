import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.db import get_db, Base
from api.main import app

ASYNNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # 非同期対応したDB接続用のengineとsessionを作成
    async_engine = create_async_engine(ASYNNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )
    
    # テスト用にオンメモリのSQLiteテーブルを初期化 (関数ごとにリセット)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    # DIを使ってFastAPI の DB の向き先をテスト用 DB に変更
    async def get_test_db():
        async with async_session() as session:
            yield session
    
    app.dependency_overrides[get_db] = get_test_db
    
    # テスト用に非同期 HTTP クライアントを返却
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_book(async_client: AsyncClient):
    # 正常なデータで本を作成
    response = await async_client.post("/books", json={
        "title": "スッキリわかるPython入門",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7",
        "total_page": 300
    })
    assert response.status_code == 200
    assert "book_id" in response.json()


@pytest.mark.asyncio
async def test_create_book_missing_field(async_client: AsyncClient):
    # 必要なフィールドが不足している場合
    response = await async_client.post("/books", json={
        "title": "スッキリわかるPython入門",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7"
    })
    assert response.status_code == 422  # バリデーションエラー


@pytest.mark.asyncio
async def test_get_books(async_client: AsyncClient):
    # 本が存在する場合
    response = await async_client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # レスポンスがリストであること


@pytest.mark.asyncio
async def test_update_book(async_client: AsyncClient):
    # 最初に本を作成してから更新テスト
    create_response = await async_client.post("/books", json={
        "title": "スッキリわかるPython入門",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7",
        "total_page": 300
    })
    book_id = create_response.json()["book_id"]

    update_response = await async_client.put(f"/books/{book_id}", json={
        "title": "スッキリわかるPythonマスター",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7",
        "total_page": 350
    })
    assert update_response.status_code == 200
    assert update_response.json()["book_id"] == book_id
    assert update_response.json()["title"] == "スッキリわかるPythonマスター"


@pytest.mark.asyncio
async def test_update_book_not_found(async_client: AsyncClient):
    # 存在しないbook_idを指定して更新しようとした場合
    response = await async_client.put("/books/999", json={
        "title": "新しい本",
        "author": "山田太郎",
        "isbn": "978-4-295-01793-7",
        "total_page": 400
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


@pytest.mark.asyncio
async def test_delete_book(async_client: AsyncClient):
    # 最初に本を作成してから削除テスト
    create_response = await async_client.post("/books", json={
        "title": "スッキリわかるPython入門",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7",
        "total_page": 300
    })
    book_id = create_response.json()["book_id"]

    delete_response = await async_client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    
    # 作成した後、本がないことを確認
    delete_response = await async_client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_book_not_found(async_client: AsyncClient):
    # 存在しないbook_idを指定して削除しようとした場合
    response = await async_client.delete("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

# GET /books/{book_id}/progress
@pytest.mark.asyncio
async def test_get_progress(async_client: AsyncClient):
    # テスト用の本を作成
    create_response = await async_client.post("/books", json={
        "title": "スッキリわかるPython入門",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7",
        "total_page": 300
    })
    assert create_response.status_code == 200
    book_id = create_response.json()["book_id"]

    # プログレスの取得を確認
    response = await async_client.get(f"/books/{book_id}/progress")
    assert response.status_code == 200
    assert response.json() == {
        "book_id": book_id,
        "current_page": 0,
        "read_time": 0,
        "read_state": "Unread",
        "start_date": None,
        "finish_date": None,
    }


# PATCH /books/{book_id}/progress
@pytest.mark.asyncio
async def test_update_progress_invalid_current_page(async_client: AsyncClient):
    # テスト用の本を作成
    create_response = await async_client.post("/books", json={
        "title": "スッキリわかるPython入門",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7",
        "total_page": 300
    })
    assert create_response.status_code == 200
    book_id = create_response.json()["book_id"]

    # プログレスを更新（current_pageがtotal_pageを超える場合）
    update_response = await async_client.patch(f"/books/{book_id}/progress", json={
        "current_page": 350,  # total_pageを超える
        "read_time": 60,
        "read_state": "Reading"
    })
    assert update_response.status_code == 400
    assert update_response.json()["detail"] == "current_page (350) cannot exceed total_page (300)"

@pytest.mark.asyncio
async def test_update_progress_invalid_read_state_transition(async_client: AsyncClient):
    # テスト用の本を作成
    create_response = await async_client.post("/books", json={
        "title": "スッキリわかるPython入門",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7",
        "total_page": 300
    })
    assert create_response.status_code == 200
    book_id = create_response.json()["book_id"]

    # プログレスを更新（read_stateが"Unread"から"Finished"に直接変更される場合）
    update_response = await async_client.patch(f"/books/{book_id}/progress", json={
        "current_page": 50,
        "read_time": 60,
        "read_state": "Finished"  # "Unread"から"Finished"に変更
    })
    assert update_response.status_code == 400
    assert update_response.json()["detail"] == 'Cannot change read_state from "Unread" to "Finished" directly.'

@pytest.mark.asyncio
async def test_update_progress_invalid_read_state_unread(async_client: AsyncClient):
    # テスト用の本を作成
    create_response = await async_client.post("/books", json={
        "title": "スッキリわかるPython入門",
        "author": "佐藤貴彦",
        "isbn": "978-4-295-01793-7",
        "total_page": 300
    })
    assert create_response.status_code == 200
    book_id = create_response.json()["book_id"]

    # プログレスを作成（"Reading"に設定）
    create_progress_response = await async_client.patch(f"/books/{book_id}/progress", json={
        "current_page": 50,
        "read_time": 60,
        "read_state": "Reading"
    })
    assert create_progress_response.status_code == 200

    # プログレスを更新（read_stateが"Reading"から"Unread"に変更される場合）
    update_response = await async_client.patch(f"/books/{book_id}/progress", json={
        "current_page": 100,
        "read_time": 60,
        "read_state": "Unread"  # "Reading"から"Unread"に変更
    })
    assert update_response.status_code == 400
    assert update_response.json()["detail"] == 'Cannot change read_state from "Reading" or "Finished" to "Unread"'

