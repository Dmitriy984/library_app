from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Book
from schemas import Book as BookSchema, BookDetail
from dependencies.auth_deps import get_librarian_user, get_admin_user

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookSchema])
async def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/{book_id}", response_model=BookDetail)
async def get_book_detail(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")
    return BookDetail(
        id=book.id, title=book.title, author=book.author,
        year=book.year, genre=book.genre, available_copies=book.available_copies,
        is_available=book.available_copies > 0, reader_name=None
    )

@router.post("/", response_model=BookSchema)
async def create_book(book_data: BookSchema, db: Session = Depends(get_db), _=Depends(get_librarian_user)):
    book = Book(**book_data.dict())
    db.add(book); db.commit(); db.refresh(book)
    return book

@router.put("/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, book_data: BookSchema, db: Session = Depends(get_db), _=Depends(get_librarian_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")
    for key, val in book_data.dict().items():
        setattr(book, key, val)
    db.commit(); db.refresh(book)
    return book

@router.delete("/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")
    db.delete(book); db.commit()
    return {"message": "Book deleted"}
