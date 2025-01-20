from pydantic import BaseModel, Field

class Book(BaseModel):
    id: int
    title: str|None = Field(None, examples=["スッキリわかるJava入門"])
    author: str|None = Field(None, examples=["中山清喬, 国本 大悟"])
    isbn: str|None = Field(None, examples=["978-4-295-01793-6"])
    total_page: int