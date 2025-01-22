from sqlalchemy.orm import Session

import api.models.book as book_model
import api.models.progress
import api.schemas.book as book_schema

def create_book(db: Session, book_create:book_schema.BookCreate) -> book_model.Book:
    book = book_model.Book(**book_create.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book