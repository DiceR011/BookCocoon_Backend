from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship

from api.db import Base

class Book(Base):
    __tablename__ = "books"
    
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=True)
    isbn = Column(String(13), nullable=True)
    total_page = Column(Integer, nullable=False)
    
    progress = relationship("Progress", back_populates="book", cascade="delete")

class Progress(Base):
    __tablename__ = "progress"
    
    book_id = Column(Integer, ForeignKey("books.book_id"), primary_key=True, index=True)
    current_page = Column(Integer, default=0, nullable=False)
    read_time = Column(Integer, default=0, nullable=False)
    read_state = Column(Enum("未読", "読書中", "読書完了"), default="未読", nullable=False)
    start_date = Column(Date, nullable=True)
    finish_date = Column(Date, nullable=True)
    
    book = relationship("Book", back_populates="progress")