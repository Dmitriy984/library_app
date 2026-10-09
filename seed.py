from database import engine, Base, SessionLocal
from models import Book, Reader, Loan, User
from data import BOOKS_DATA, READERS_DATA, LOANS_DATA, USERS_DATA
from datetime import datetime
from auth import get_password_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(Loan).delete()
        db.query(Book).delete()
        db.query(Reader).delete()
        db.query(User).delete()
        db.commit()

        for item in BOOKS_DATA:
            db.add(Book(**item))
        db.commit()

        for item in READERS_DATA:
            reader = Reader(**item)
            db.add(reader)
        db.commit()

        for reader_id, book_id, taken_str, returned_str in LOANS_DATA:
            taken = datetime.fromisoformat(taken_str)
            returned = datetime.fromisoformat(returned_str) if returned_str else None
            loan = Loan(
                reader_id=reader_id,
                book_id=book_id,
                taken_at=taken,
                returned_at=returned
            )
            db.add(loan)
        db.commit()

        for u in USERS_DATA:
            user = User(
                username=u["username"],
                email=u["email"],
                password_hash=get_password_hash(u["password"]),
                role=u["role"]
            )
            db.add(user)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
    print("Database seeded successfully.")
