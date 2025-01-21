from fastapi import FastAPI

from api.routers import book, progress

app = FastAPI()

app.include_router(book.router)
app.include_router(progress.router)