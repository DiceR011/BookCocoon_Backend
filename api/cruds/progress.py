from sqlalchemy import select
from sqlalchemy.engine import Result
from lib.time_JST import get_japan_time
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.book
import api.models.progress as progress_model
import api.schemas.progress as progress_schema

# Read
async def get_progress(db: AsyncSession, book_id: int) -> progress_model.Progress | None:
    result: Result = await db.execute(
        select(progress_model.Progress).filter(progress_model.Progress.book_id == book_id)
    )
    
    return result.scalars().first()

# Update
async def patch_progress(db: AsyncSession, progress_patch: progress_schema.ProgressUpdate, original: progress_model.Progress) -> progress_model.Progress:
    # current_pageがbook.total_pageを超える場合のエラー
    if original.book and progress_patch.current_page > original.book.total_page:
        raise ValueError(f"current_page ({progress_patch.current_page}) cannot exceed total_page ({original.book.total_page})")

    # read_stateが"Unread"から"Finished"に直接変更された場合のエラー
    if original.read_state == "Unread" and progress_patch.read_state == "Finished":
        raise ValueError('Cannot change read_state from "Unread" to "Finished" directly.')
    
    # read_stateが"Reading","Finish"から"Unread"に変更された場合のエラー
    if original.read_state in ["Reading", "Finished"] and progress_patch.read_state == "Unread":
        raise ValueError('Cannot change read_state from "Reading" or "Finished" to "Unread"')
    
    # book の Lazy Loading 確認（必要に応じてリフレッシュ）
    if not original.book:
        await db.refresh(original, ["book"])
    
    # read_stateが"Unread"から"Reading"になった場合、start_dateに時間を記録
    if original.read_state == "Unread" and progress_patch.read_state == "Reading":
        original.start_date = get_japan_time()
    
    # read_stateが"Finished"になった場合、finish_dateに時間を記録
    if progress_patch.read_state == "Finished":
        original.finish_date = get_japan_time()
    
    original.current_page = progress_patch.current_page
    original.read_time = progress_patch.read_time
    original.read_state = progress_patch.read_state
    db.add(original)
    await db.commit()
    await db.refresh(original)
    
    return original