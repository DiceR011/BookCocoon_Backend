from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.cruds.book as book_crud
from api.db import get_db
import api.schemas.book as book_schema

router = APIRouter()

@router.get("/books",response_model=list[book_schema.Book])
async def list_books():
    return [book_schema.Book(book_id=1,title="一冊目の本",author="REI",isbn="000-0-000-0000-0",total_page=1)]

@router.post("/books",response_model=book_schema.BookCreateResponse)
async def create_book(book_body: book_schema.BookCreate, db: Session = Depends(get_db)):
    return book_crud.create_book(db, book_body)

@router.put("/books/{book_id}",response_model=book_schema.BookCreateResponse)
async def update_book(book_id: int, book_body: book_schema.BookCreate):
    return book_schema.BookCreateResponse(book_id=book_id, **book_body.dict())

@router .delete("/books/{book_id}", response_model=None)
async def delete_book(book_id: int):
    return