from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Reader, Loan, Book
from schemas import ReaderCreate, ReaderUpdate, ReaderResponse, ReaderProfile, LoanWithBook, BookResponse
from dependencies.auth_deps import get_librarian_or_admin, get_admin_user

router = APIRouter(prefix="/readers", tags=["readers"])

@router.get("/", response_model=List[ReaderResponse])
async def get_readers(
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    return db.query(Reader).all()

@router.get("/{reader_id}", response_model=ReaderProfile)
async def get_reader_profile(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    loans = db.query(Loan).filter(Loan.reader_id == reader_id).all()
    history = []
    for loan in loans:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        if book:
            history.append(LoanWithBook(
                id=loan.id,
                book=BookResponse.from_orm(book),
                taken_at=loan.taken_at,
                returned_at=loan.returned_at
            ))
    return ReaderProfile(
        id=reader.id,
        full_name=reader.full_name,
        email=reader.email,
        phone=reader.phone,
        registration_date=reader.registration_date,
        reading_history=history
    )

@router.get("/{reader_id}/books", response_model=List[LoanWithBook])
async def get_current_loans(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    active_loans = db.query(Loan).filter(Loan.reader_id == reader_id, Loan.returned_at.is_(None)).all()
    result = []
    for loan in active_loans:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        if book:
            result.append(LoanWithBook(
                id=loan.id,
                book=BookResponse.from_orm(book),
                taken_at=loan.taken_at,
                returned_at=loan.returned_at
            ))
    return result

@router.post("/", response_model=ReaderResponse, status_code=201)
async def create_reader(
    reader_data: ReaderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    reader = Reader(**reader_data.dict())
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader

@router.put("/{reader_id}", response_model=ReaderResponse)
async def update_reader(
    reader_id: int,
    reader_data: ReaderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_librarian_or_admin)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    for field, value in reader_data.dict(exclude_unset=True).items():
        setattr(reader, field, value)
    db.commit()
    db.refresh(reader)
    return reader

@router.delete("/{reader_id}")
async def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    active_loans = db.query(Loan).filter(Loan.reader_id == reader_id, Loan.returned_at.is_(None)).count()
    if active_loans > 0:
        raise HTTPException(status_code=400, detail="Cannot delete reader with unreturned books")
    db.delete(reader)
    db.commit()
    return {"message": "Reader deleted"}
