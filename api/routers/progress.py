from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.progress as progress_crud
import api.cruds.book as book_crud
from api.db import get_db
import api.schemas.progress as progress_schema

router = APIRouter()

@router.get("/books/{book_id}/progress", response_model=progress_schema.ProgressResponse)
async def get_progress(book_id: int, db: AsyncSession = Depends(get_db)):
    progress = await progress_crud.get_progress(db, book_id=book_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Book not found")
    return progress

@router.patch("/books/{book_id}/progress",response_model=progress_schema.ProgressResponse)
async def update_progress(book_id: int, update_data: progress_schema.ProgressUpdate, db: AsyncSession = Depends(get_db)):
    progress = await progress_crud.get_progress(db, book_id=book_id)
    book = await book_crud.get_book(db, book_id=book_id)

    if not progress:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 現在のページが全体ページより大きくなった場合のエラー
    if update_data.current_page > book.total_page:
        raise HTTPException(status_code=400, detail=f"current_page ({update_data.current_page}) cannot exceed total_page ({book.total_page})")
    
    # read_stateが"Unread"から"Finshed"に変更された場合のエラー
    if update_data.read_state == "Finished" and progress.read_state == "Unread":
         raise HTTPException(status_code=400, detail='Cannot change read_state from "Unread" to "Finished" directly.')
    
    # read_stateが"Reading","Finished"から"Unred"に変更された場合のエラー
    if update_data.read_state == "Unread" and (progress.read_state == "Reading" or progress.read_state == "Finished"):
        raise HTTPException(status_code=400, detail='Cannot change read_state from "Reading" or "Finished" to "Unread"')

    return await progress_crud.patch_progress(db, update_data, original=progress)