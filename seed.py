
from database import engine, Base, SessionLocal
from models import Book, Reader, reader_books
from data import BOOKS_DATA, READERS_DATA, HISTORY_DATA
from datetime import date

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.execute(reader_books.delete())
        db.query(Book).delete()
        db.query(Reader).delete()
        db.commit()

        for item in BOOKS_DATA:
            book = Book(**item)
            db.add(book)
        db.commit()

        for item in READERS_DATA:
            reader = Reader(full_name=item["full_name"], email=item["email"], phone=item["phone"],
                            registration_date=date.fromisoformat(item["registration_date"]))
            db.add(reader)
        db.commit()

        for reader_id, book_id, taken_str, returned_str in HISTORY_DATA:
            taken = date.fromisoformat(taken_str)
            returned = date.fromisoformat(returned_str) if returned_str else None
            db.execute(reader_books.insert().values(
                reader_id=reader_id,
                book_id=book_id,
                taken_at=taken,
                returned_at=returned
            ))
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
    print("База данных заполнена.")
