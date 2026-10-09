from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date

class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    available_copies: int = 1

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    available_copies: Optional[int] = None

class BookResponse(BookBase):
    id: int
    class Config:
        from_attributes = True

class BookDetail(BookResponse):
    is_available: bool
    reader_name: Optional[str] = None

class ReaderBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    registration_date: Optional[date] = None

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ReaderResponse(ReaderBase):
    id: int
    class Config:
        from_attributes = True

class ReaderProfile(ReaderResponse):
    reading_history: List["LoanWithBook"] = []

class LoanWithBook(BaseModel):
    id: int
    book: BookResponse
    taken_at: datetime
    returned_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class LoanCreate(BaseModel):
    reader_id: int
    book_id: int

class LoanResponse(BaseModel):
    id: int
    reader_id: int
    book_id: int
    taken_at: datetime
    returned_at: Optional[datetime] = None
    reader: ReaderResponse
    book: BookResponse
    class Config:
        from_attributes = True

class LoanActiveResponse(BaseModel):
    id: int
    reader_id: int
    book_id: int
    taken_at: datetime
    reader: ReaderResponse
    book: BookResponse
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, regex="^[a-zA-Z0-9_]+$")
    email: EmailStr
    role: str = "librarian"

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    reader_id: Optional[int] = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)
