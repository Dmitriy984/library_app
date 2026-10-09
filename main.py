from fastapi import FastAPI, HTTPException
from typing import List
from schemas import Book, BookDetail, Reader, ReaderProfile

books_db = [
    BookDetail(id=1, title="Война и мир", author="Лев Толстой", year=1869, is_available=False, reader_name="Иван Петров"),
    BookDetail(id=2, title="Преступление и наказание", author="Фёдор Достоевский", year=1866, is_available=True, reader_name=None),
    BookDetail(id=3, title="Мастер и Маргарита", author="Михаил Булгаков", year=1967, is_available=False, reader_name="Мария Смирнова"),
]

readers_db = [
    Reader(id=1, name="Иван Петров", reading_history=[1, 2]),
    Reader(id=2, name="Мария Смирнова", reading_history=[2, 3]),
    Reader(id=3, name="Алексей Иванов", reading_history=[1, 3]),
]

def get_book_by_id(book_id: int) -> BookDetail | None:
    return next((b for b in books_db if b.id == book_id), None)

def get_reader_by_id(reader_id: int) -> Reader | None:
    return next((r for r in readers_db if r.id == reader_id), None)

app = FastAPI(title="Библиотека")

@app.get("/books", response_model=List[Book])
async def get_books():
    return books_db

@app.get("/readers", response_model=List[Reader])
async def get_readers():
    return readers_db

@app.get("/readers/{reader_id}", response_model=ReaderProfile)
async def get_reader_profile(reader_id: int):
    reader = get_reader_by_id(reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    books_read = []
    for book_id in reader.reading_history:
        book = get_book_by_id(book_id)
        if book:
            books_read.append(Book(id=book.id, title=book.title, author=book.author, year=book.year))
    return ReaderProfile(id=reader.id, name=reader.name, reading_history=books_read)

@app.get("/books/{book_id}", response_model=BookDetail)
async def get_book_detail(book_id: int):
    book = get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book
