from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result
from lib.time_JST import get_japan_time
from enum import Enum

import api.models.book
import api.models.progress as progress_model
import api.schemas.progress as progress_schema

# Read
def get_progress(db: Session, book_id: int) -> progress_model.Progress | None:
    result: Result = db.execute(
        select(progress_model.Progress).filter(progress_model.Progress.book_id == book_id)
    )
    
    return result.scalars().first()

# Update
def patch_progress(db: Session, progress_patch: progress_schema.ProgressUpdate, original: progress_model.Progress) -> progress_model.Progress:
    # read_stateが"Unread"から、"Reading"になった場合、start_dateに時間を記録
    if original.read_state == "Unread" and progress_patch.read_state == "Reading":
        original.start_date = get_japan_time()
    
    # read_stateが"Finished"になった場合、finish_dateに時間を記録
    if progress_patch.read_state == "Finished":
        original.finish_date = get_japan_time()
    
    original.current_page = progress_patch.current_page
    original.read_time = progress_patch.read_time
    original.read_state = progress_patch.read_state
    db.add(original)
    db.commit()
    db.refresh(original)
    
    return original