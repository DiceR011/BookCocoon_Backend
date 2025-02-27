from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.book as book_crud
from api.db import get_db
import api.schemas.book as book_schema

router = APIRouter()

@router.get("/books",response_model=list[book_schema.Book])
async def list_books(db: AsyncSession = Depends(get_db)):
    return await book_crud.get_books(db)

@router.post("/books",response_model=book_schema.BookCreateResponse)
async def create_book(book_body: book_schema.BookCreate, db: AsyncSession = Depends(get_db)):
    return await book_crud.create_book(db, book_body)

@router.put("/books/{book_id}",response_model=book_schema.BookCreateResponse)
async def update_book(book_id: int, book_body: book_schema.BookCreate, db: AsyncSession = Depends(get_db)):
    book = await book_crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return await book_crud.update_book(db, book_body, original=book)

@router.delete("/books/{book_id}", response_model=None)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return await book_crud.delete_book(db, original=book)


