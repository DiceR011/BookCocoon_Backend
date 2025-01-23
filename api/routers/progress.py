from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.progress as progress_crud
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
    if not progress:
        raise HTTPException(status_code=404, detail="Book not found")
    
    
    try:
        return await progress_crud.patch_progress(db, update_data, original=progress)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))