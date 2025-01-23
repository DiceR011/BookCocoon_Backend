from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ReadState(str, Enum):
    UNREAD = "Unread"
    READING = "Reading"
    COMPLETED = "Finished"


# 共通スキーマ
class ProgressBase(BaseModel):
    book_id: int
    current_page: int
    read_time: int
    read_state: ReadState = Field(..., description="読書の進行状態")
    start_date: datetime | None = Field(None, description="読書開始日")
    finish_date: datetime | None = Field(None, description="読書完了日")



# リクエストスキーマ
class ProgressUpdate(BaseModel):
    current_page: int | None = Field(None, description="現在のページ")
    read_time: int | None = Field(None, description="読書時間（秒単位）")
    read_state: ReadState | None = Field(None, description="読書状態の変更")


# レスポンススキーマ
class ProgressResponse(ProgressBase):
    class Config:
        orm_mode = True
