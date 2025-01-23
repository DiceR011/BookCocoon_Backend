from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from lib.time_JST import get_japan_time

from api.db import Base

class Book(Base):
    __tablename__ = "books"
    
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=True)
    isbn = Column(String(17), nullable=True)
    total_page = Column(Integer, nullable=False)
    time_stamp =  Column(DateTime, default=lambda: get_japan_time(), nullable=False)
    
    progress = relationship("Progress", back_populates="book", cascade="delete")