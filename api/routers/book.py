from fastapi import APIRouter

router = APIRouter()

@router.get("/books")
async def list_books():
    pass

@router.post("/books")
async def create_book():
    pass

@router.put("/books/{book_id}")
async def update_book():
    pass

@router .delete("/books/{book_id}")
async def delete_book():
    pass