from fastapi import APIRouter, HTTPException
from datetime import date
import api.schemas.progress as progress_schema

router = APIRouter()

# 仮データ
progress_data = {
    1: {
        "book_id": 1,
        "current_page": 0,
        "read_time": 0,
        "read_state": "未読",
        "start_date": None,
        "finish_date": None,
    }
}


@router.get("/books/{book_id}/progress", response_model=progress_schema.ProgressResponse)
async def get_progress(book_id: int):
    progress = progress_data.get(book_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Book not found")
    return progress

@router.patch("/books/{book_id}/progress",response_model=progress_schema.ProgressResponse)
async def update_progress(book_id: int, update_data: progress_schema.ProgressUpdate):
    progress = progress_data(book_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 状態遷移のロジック
    if update_data.read_state:
        if update_data.read_state == "読書中" and progress["read_state"] == "未読":
            progress["start_date"] = date.today()
        elif update_data.read_state == "読書完了" and progress["read_state"] == "読書中":
            progress["finish_date"] = date.today()
        
        progress["read_state"] = update_data.read_state
    
    # 他のフィールドの更新
    if update_data.current_page is not None:
        progress["current_page"] = update_data.current_page
    
    if update_data.read_time is not None:
        progress["read_time"] = update_data.read_time
    
    return progress