from fastapi import FastAPI

from api.routers import book, readingprogress

app = FastAPI()

app.include_router(book.router)
app.include_router(readingprogress.router)