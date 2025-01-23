from sqlalchemy.orm import Session
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.book as book_model
import api.models.progress as progress_model
import api.schemas.book as book_schema

def get_book(db: Session, book_id: int) -> book_model.Book | None:
    result: Result = db.execute(
        select(book_model.Book).filter(book_model.Book.book_id == book_id)
        )
    
    return result.scalars().first()

# Create,作成されると同時にprogressのレコードも作成される
def create_book(db: Session, book_create:book_schema.BookCreate) -> book_model.Book:
    book = book_model.Book(**book_create.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    
    # 新しい本に対するProgressレコードの作成
    new_progress = progress_model.Progress(
        book_id = book.book_id,
        start_date = None,
        finish_date = None,
    )
    
    db.add(new_progress)
    db.commit()
    
    return book

# Read
def get_books(db: Session) -> list[tuple[int, str, str, str, PositiveInt]]:
    result: Result = db.execute(
        select(
            book_model.Book.book_id,
            book_model.Book.title,
            book_model.Book.author,
            book_model.Book.isbn,
            book_model.Book.total_page,
            book_model.Book.time_stamp
        )
    )
    
    return result.all()

# Update
def update_book(
    db: Session, book_create: book_schema.BookCreate, original: book_model.Book
    ) ->book_model.Book:
    original.title = book_create.title
    original.author = book_create.author
    original.isbn = book_create.isbn
    original.total_page = book_create.total_page
    db.add(original)
    db.commit()
    db.refresh(original)
    
    return original

# Delete
def delete_book(db: Session, original: book_model.Book) -> None:
    db.delete(original)
    db.commit()