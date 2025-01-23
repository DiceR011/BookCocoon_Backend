from pydantic import BaseModel, Field, PositiveInt
from datetime import datetime

# 共通スキーマ
class BookBase(BaseModel):
    title: str | None = Field(
        None,
        examples=["スッキリわかるJava入門"],
        description="本のタイトル"
    )
    author: str | None = Field(
        None,
        examples=["中山清喬, 国本 大悟"],
        description="著者名（複数名の場合はカンマ区切り）"
    )
    isbn: str | None = Field(
        None,
        examples=["978-4-295-01793-6"],
        description="ISBNコード"
    )
    total_page: PositiveInt = Field(
        ...,
        description="本の総ページ数（正の整数）"
    )


# 全体スキーマ
class Book(BookBase):
    book_id: int
    time_stamp: datetime

    class Config:
        orm_mode = True


# リクエストスキーマ
class BookCreate(BookBase):
    pass


# レスポンススキーマ
class BookCreateResponse(BaseModel):
    book_id: int

    class Config:
        orm_mode = True
