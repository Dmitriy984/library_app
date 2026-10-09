from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Reader, Book, reader_books
from schemas import Reader as ReaderSchema, ReaderProfile, Book as BookSchema
from dependencies.auth_deps import get_librarian_user, get_admin_user

router = APIRouter(prefix="/readers", tags=["readers"])

@router.get("/", response_model=List[ReaderSchema])
async def get_readers(
    db: Session = Depends(get_db),
    current_user=Depends(get_librarian_user)
):
    return db.query(Reader).all()

@router.get("/{reader_id}", response_model=ReaderProfile)
async def get_reader_profile(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_librarian_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    history_books = (
        db.query(Book)
        .join(reader_books, Book.id == reader_books.c.book_id)
        .filter(reader_books.c.reader_id == reader_id)
        .all()
    )
    return ReaderProfile(
        id=reader.id,
        full_name=reader.full_name,
        email=reader.email,
        phone=reader.phone,
        registration_date=reader.registration_date,
        reading_history=[BookSchema.from_orm(b) for b in history_books]
    )

@router.post("/", response_model=ReaderSchema)
async def create_reader(
    reader_data: ReaderSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_librarian_user)
):
    reader = Reader(**reader_data.dict())
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader

@router.put("/{reader_id}", response_model=ReaderSchema)
async def update_reader(
    reader_id: int,
    reader_data: ReaderSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_librarian_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    for key, value in reader_data.dict().items():
        setattr(reader, key, value)
    db.commit()
    db.refresh(reader)
    return reader

@router.delete("/{reader_id}")
async def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_admin_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    db.delete(reader)
    db.commit()
    return {"message": "Reader deleted"}
