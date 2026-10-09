from datetime import date

BOOKS_DATA = [
    {"title": "Война и мир", "author": "Лев Толстой", "isbn": "978-5-17-123456-1", "year": 1869, "genre": "Роман", "available_copies": 3},
    {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "isbn": "978-5-17-123456-2", "year": 1866, "genre": "Роман", "available_copies": 2},
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "isbn": "978-5-17-123456-3", "year": 1967, "genre": "Роман", "available_copies": 1},
    {"title": "Евгений Онегин", "author": "Александр Пушкин", "isbn": "978-5-17-123456-4", "year": 1833, "genre": "Роман в стихах", "available_copies": 4},
    {"title": "Анна Каренина", "author": "Лев Толстой", "isbn": "978-5-17-123456-5", "year": 1877, "genre": "Роман", "available_copies": 2},
    {"title": "Собачье сердце", "author": "Михаил Булгаков", "isbn": "978-5-17-123456-6", "year": 1925, "genre": "Повесть", "available_copies": 1},
    {"title": "Тихий Дон", "author": "Михаил Шолохов", "isbn": "978-5-17-123456-7", "year": 1940, "genre": "Роман-эпопея", "available_copies": 2},
]

READERS_DATA = [
    {"full_name": "Иван Петров", "email": "ivan@mail.ru", "phone": "+7-999-111-22-33", "registration_date": date(2023, 1, 15)},
    {"full_name": "Мария Смирнова", "email": "maria@mail.ru", "phone": "+7-999-222-33-44", "registration_date": date(2023, 2, 20)},
    {"full_name": "Алексей Иванов", "email": "alex@mail.ru", "phone": "+7-999-333-44-55", "registration_date": date(2023, 3, 10)},
    {"full_name": "Елена Кузнецова", "email": "elena@mail.ru", "phone": "+7-999-444-55-66", "registration_date": date(2023, 4, 5)},
    {"full_name": "Дмитрий Новиков", "email": "dmitry@mail.ru", "phone": "+7-999-555-66-77", "registration_date": date(2023, 5, 12)},
]

LOANS_DATA = [
    (1, 1, "2023-06-01", "2023-06-15"),
    (1, 2, "2023-07-01", None),
    (1, 3, "2023-08-01", "2023-08-20"),
    (2, 2, "2023-06-10", "2023-06-25"),
    (2, 4, "2023-07-15", None),
    (2, 5, "2023-09-01", "2023-09-10"),
    (2, 1, "2023-10-01", None),
    (3, 1, "2023-05-01", "2023-05-20"),
    (3, 3, "2023-06-01", "2023-06-10"),
    (3, 6, "2023-08-01", None),
    (3, 7, "2023-09-01", "2023-09-15"),
    (4, 4, "2023-04-01", "2023-04-20"),
    (4, 5, "2023-05-01", None),
    (4, 7, "2023-06-01", "2023-06-15"),
    (4, 2, "2023-07-01", None),
    (5, 3, "2023-06-01", "2023-06-20"),
    (5, 6, "2023-07-01", "2023-07-15"),
    (5, 1, "2023-08-01", None),
    (5, 5, "2023-09-01", "2023-09-25"),
]

USERS_DATA = [
    {"username": "admin", "email": "admin@library.ru", "password": "admin123", "role": "admin"},
    {"username": "librarian1", "email": "lib1@library.ru", "password": "lib12345", "role": "librarian"},
    {"username": "librarian2", "email": "lib2@library.ru", "password": "lib67890", "role": "librarian"},
]
