from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.cruds.progress as progress_crud
from api.db import get_db
import api.schemas.progress as progress_schema

router = APIRouter()

@router.get("/books/{book_id}/progress", response_model=progress_schema.ProgressResponse)
async def get_progress(book_id: int, db: Session = Depends(get_db)):
    progress = progress_crud.get_progress(db, book_id=book_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Book not found")
    return progress

@router.patch("/books/{book_id}/progress",response_model=progress_schema.ProgressResponse)
async def update_progress(book_id: int, update_data: progress_schema.ProgressUpdate, db: Session = Depends(get_db)):
    progress = progress_crud.get_progress(db, book_id=book_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Book not found")
    
    
    try:
        return progress_crud.patch_progress(db, update_data, original=progress)
    except ValueError as e:
        # ValueErrorをHTTP 400エラーに変換
        raise HTTPException(status_code=400, detail=str(e))