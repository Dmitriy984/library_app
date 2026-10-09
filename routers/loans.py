from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models import Loan, Book, Reader
from schemas import LoanCreate, LoanResponse, LoanActiveResponse, BookResponse, ReaderResponse
from dependencies.auth_deps import get_librarian_or_admin

router = APIRouter(prefix="/loans", tags=["loans"])

@router.get("/", response_model=List[LoanResponse])
async def get_all_loans(
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    loans = db.query(Loan).all()
    result = []
    for loan in loans:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
        if book and reader:
            result.append(LoanResponse(
                id=loan.id,
                reader_id=loan.reader_id,
                book_id=loan.book_id,
                taken_at=loan.taken_at,
                returned_at=loan.returned_at,
                reader=ReaderResponse.from_orm(reader),
                book=BookResponse.from_orm(book)
            ))
    return result

@router.get("/active", response_model=List[LoanActiveResponse])
async def get_active_loans(
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    active = db.query(Loan).filter(Loan.returned_at.is_(None)).all()
    result = []
    for loan in active:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
        if book and reader:
            result.append(LoanActiveResponse(
                id=loan.id,
                reader_id=loan.reader_id,
                book_id=loan.book_id,
                taken_at=loan.taken_at,
                reader=ReaderResponse.from_orm(reader),
                book=BookResponse.from_orm(book)
            ))
    return result

@router.post("/", response_model=LoanResponse, status_code=201)
async def create_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    reader = db.query(Reader).filter(Reader.id == loan_data.reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    book = db.query(Book).filter(Book.id == loan_data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")
    book.available_copies -= 1
    loan = Loan(
        reader_id=loan_data.reader_id,
        book_id=loan_data.book_id,
        taken_at=datetime.utcnow(),
        returned_at=None
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return LoanResponse(
        id=loan.id,
        reader_id=loan.reader_id,
        book_id=loan.book_id,
        taken_at=loan.taken_at,
        returned_at=loan.returned_at,
        reader=ReaderResponse.from_orm(reader),
        book=BookResponse.from_orm(book)
    )

@router.post("/{loan_id}/return", response_model=LoanResponse)
async def return_book(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.returned_at is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    loan.returned_at = datetime.utcnow()
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if book:
        book.available_copies += 1
    db.commit()
    db.refresh(loan)
    reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
    return LoanResponse(
        id=loan.id,
        reader_id=loan.reader_id,
        book_id=loan.book_id,
        taken_at=loan.taken_at,
        returned_at=loan.returned_at,
        reader=ReaderResponse.from_orm(reader),
        book=BookResponse.from_orm(book)
    )
