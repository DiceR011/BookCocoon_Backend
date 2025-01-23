from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from api.db import Base

class Progress(Base):
    __tablename__ = "progress"
    
    book_id = Column(Integer, ForeignKey("books.book_id"), primary_key=True, index=True)
    current_page = Column(Integer, default=0, nullable=False)
    read_time = Column(Integer, default=0, nullable=False)
    read_state = Column(Enum("Unread", "Reading", "Finished"), default="Unread", nullable=False)
    start_date = Column(DateTime, nullable=True)
    finish_date = Column(DateTime, nullable=True)
    
    book = relationship("Book", back_populates="progress")