from pydantic import BaseModel
from typing import List, Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

class Reader(BaseModel):
    id: int
    name: str
    reading_history: List[int]

class BookDetail(Book):
    is_available: bool
    reader_name: Optional[str]

class ReaderProfile(Reader):
    reading_history: List[Book]
