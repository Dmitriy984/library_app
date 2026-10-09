from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, datetime

reader_books = Table(
    "reader_books",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("reader_id", Integer, ForeignKey("readers.id")),
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("taken_at", Date, nullable=False),
    Column("returned_at", Date, nullable=True),
)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    available_copies = Column(Integer, default=1)
    readers = relationship("Reader", secondary=reader_books, back_populates="books")

class Reader(Base):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    registration_date = Column(Date, default=date.today)
    books = relationship("Book", secondary=reader_books, back_populates="readers")

class User(Base):
    def verify_password(self, plain_password: str) -> bool:
        from auth import verify_password
        return verify_password(plain_password, self.password_hash)
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="librarian") 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  

