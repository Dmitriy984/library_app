from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, datetime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    available_copies = Column(Integer, default=1)
    loans = relationship("Loan", back_populates="book")

class Reader(Base):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    registration_date = Column(Date, default=date.today)
    loans = relationship("Loan", back_populates="reader")

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    taken_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    returned_at = Column(DateTime, nullable=True)
    reader = relationship("Reader", back_populates="loans")
    book = relationship("Book", back_populates="loans")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="librarian")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
