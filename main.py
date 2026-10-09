from fastapi import FastAPI, HTTPException
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

class ReaderProfile(BaseModel):
    id: int
    name: str
    reading_history: List[Book] 

books_db = [
    Book(id=1, title="Война и мир", author="Лев Толстой", year=1869),
    Book(id=2, title="Преступление и наказание", author="Фёдор Достоевский", year=1866),
    Book(id=3, title="Мастер и Маргарита", author="Михаил Булгаков", year=1967),
]

readers_db = [
    Reader(id=1, name="Иван Петров", reading_history=[1, 2]),
    Reader(id=2, name="Мария Смирнова", reading_history=[2, 3]),
    Reader(id=3, name="Алексей Иванов", reading_history=[1, 3]),
]

app = FastAPI(title="Библиотека", description="Простое API для управления библиотекой")

@app.get("/books", response_model=List[Book])
async def get_books():
    return books_db

@app.get("/readers", response_model=List[Reader])
async def get_readers():
    return readers_db

@app.get("/readers/{reader_id}", response_model=ReaderProfile)
async def get_reader_profile(reader_id: int):

    reader = next((r for r in readers_db if r.id == reader_id), None)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    books_read = []
    for book_id in reader.reading_history:
        book = next((b for b in books_db if b.id == book_id), None)
        if book:
            books_read.append(book)

    return ReaderProfile(id=reader.id, name=reader.name, reading_history=books_read)

@app.get("/books/{book_id}", response_model=Book)
async def get_book_detail(book_id: int):
    book = next((b for b in books_db if b.id == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book
