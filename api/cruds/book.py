from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.book as book_model
import api.models.progress as progress_model
import api.schemas.book as book_schema

async def get_book(db: AsyncSession, book_id: int) -> book_model.Book | None:
    result: Result = await db.execute(
        select(book_model.Book).filter(book_model.Book.book_id == book_id)
        )
    
    return result.scalars().first()

# Create,作成されると同時にprogressのレコードも作成される
async def create_book(db: AsyncSession, book_create:book_schema.BookCreate) -> book_model.Book:
    book = book_model.Book(**book_create.dict())
    db.add(book)
    await db.commit()
    await db.refresh(book)
    
    # 新しい本に対するProgressレコードの作成
    new_progress = progress_model.Progress(
        book_id = book.book_id,
        start_date = None,
        finish_date = None,
    )
    
    db.add(new_progress)
    await db.commit()  
    await db.refresh(book)  
    
    return book

# Read
async def get_books(db: AsyncSession) -> list[tuple[int, str, str, str, PositiveInt]]:
    result: Result = await db.execute(
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
async def update_book(
    db: AsyncSession, book_create: book_schema.BookCreate, original: book_model.Book
    ) ->book_model.Book:
    original.title = book_create.title
    original.author = book_create.author
    original.isbn = book_create.isbn
    original.total_page = book_create.total_page
    db.add(original)
    await db.commit()
    await db.refresh(original)
    
    return original

# Delete
async def delete_book(db: AsyncSession, original: book_model.Book) -> None:
    await db.delete(original)
    await db.commit()