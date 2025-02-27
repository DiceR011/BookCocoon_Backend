from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import book, library, progress

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


app.include_router(book.router)
app.include_router(progress.router)
app.include_router(library.router)