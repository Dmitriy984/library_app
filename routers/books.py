from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Book
from schemas import BookCreate, BookUpdate, BookResponse, BookDetail
from dependencies.auth_deps import get_librarian_or_admin, get_admin_user

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
async def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/search", response_model=List[BookResponse])
async def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    return query.all()

@router.get("/available", response_model=List[BookResponse])
async def get_available_books(db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.available_copies > 0).all()

@router.get("/{book_id}", response_model=BookDetail)
async def get_book_detail(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    is_available = book.available_copies > 0
    return BookDetail(
        id=book.id,
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        year=book.year,
        genre=book.genre,
        available_copies=book.available_copies,
        is_available=is_available,
        reader_name=None
    )

@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    book = Book(**book_data.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in book_data.dict(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}
