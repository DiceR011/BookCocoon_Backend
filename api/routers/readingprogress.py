from fastapi import APIRouter

router = APIRouter()

@router.get("/books/{book_id}/read_time")
async def read_time():
    pass

@router.patch("/books/{book_id}/read_time")
async def update_read_time():
    pass

@router.get("/books/{book_id}/current_page")
async def current_page():
    pass

@router.patch("/books/{book_id}/current_page")
async def update_current_page():
    pass