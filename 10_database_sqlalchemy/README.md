# 📌 Module 10 — Database Integration: SQLite & SQLAlchemy

This module covers connecting a FastAPI application to a database. We explore two different approaches:
1. **Direct SQLite connection** using the built-in `sqlite3` driver.
2. **SQLAlchemy ORM** to map Python classes directly to database tables.

---

## 🧠 Database Choices: SQLite

**SQLite** is a lightweight, serverless relational database engine. It stores data in a single local file (e.g., `test.db`). It requires no configuration, making it perfect for development and learning.

---

## ⚔️ SQLite (Direct) vs SQLAlchemy (ORM)

| Feature | Direct SQLite (`sqlite3`) | SQLAlchemy (ORM) |
|---|---|---|
| **What is it?** | A raw database driver. | Object-Relational Mapper (ORM). |
| **How to write queries?** | Raw SQL strings: `SELECT * FROM todos`. | Python objects & methods: `db.query(Todo).all()`. |
| **Setup Complexity** | Very Low. | Medium. |
| **Type Safety & Auto-complete**| Low (queries are plain text strings). | High (uses Python classes). |
| **Database Portability** | Hard to switch to other databases. | Easy (change connection string). |

---

## 📁 Folder Structure

```
10_database_sqlalchemy/
├── README.md               ← You are here
├── sqlite_example.py       ← Direct SQLite connection example
└── sqlalchemy_example.py   ← SQLAlchemy ORM connection example
```

---

## 1️⃣ Direct SQLite Example (`sqlite_example.py`)

Using raw Python `sqlite3`, we manually handle opening connections, cursors, executing SQL strings, committing changes, and parsing raw tuple results into dictionaries.

```python
import sqlite3
from fastapi import FastAPI

app = FastAPI()

# Connect to database (check_same_thread=False is required for multi-threaded uvicorn)
conn = sqlite3.connect("sqlite_test.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0
)
""")
conn.commit()
```

---

## 2️⃣ SQLAlchemy ORM Example (`sqlalchemy_example.py`)

With SQLAlchemy, we define models using Python classes and map database sessions cleanly to API requests using FastAPI's dependency injection (`Depends`).

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Depends

DATABASE_URL = "sqlite:///./sqlalchemy_test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)
```

We yield db sessions in requests using a dependency:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## ▶️ How to Run

### Run SQLite direct API:
```bash
cd 10_database_sqlalchemy
uvicorn sqlite_example:app --reload --port 8000
```

### Run SQLAlchemy ORM API:
```bash
cd 10_database_sqlalchemy
uvicorn sqlalchemy_example:app --reload --port 8000
```

---

## 🎯 Interview Questions

**Q1. What is SQLite and when should you use it?**
> SQLite is a serverless, self-contained relational database system that stores the database in a single file on disk. It is ideal for local development, testing, prototypes, mobile apps, and low-traffic sites because it requires zero installation or configuration.

**Q2. Why do we need `check_same_thread=False` when connecting to SQLite in FastAPI?**
> By default, SQLite only allows one thread to communicate with it. Since FastAPI handles concurrent requests across multiple threads, we must set `check_same_thread=False` to prevent it from throwing exceptions when multiple requests access the database at the same time.

**Q3. What is an ORM (Object-Relational Mapper)?**
> An ORM is a tool that lets you interact with a relational database using your programming language's objects (classes and methods) instead of writing raw SQL queries. SQLAlchemy is the standard ORM used in Python.

**Q4. What is the role of `declarative_base()` in SQLAlchemy?**
> `declarative_base()` returns a base class. We inherit from this base class to create our SQLAlchemy models (like `class Todo(Base)`). SQLAlchemy uses this base class to keep track of all database models we register, allowing it to create the tables in the database automatically.

**Q5. What is the difference between `create_engine` and `sessionmaker` in SQLAlchemy?**
> `create_engine` establishes the physical connection pool to the database. `sessionmaker` acts as a factory to create individual database session objects (`SessionLocal`). Sessions are used to execute transactions and queries, which are eventually committed back to the database through the engine.

**Q6. Why is it important to close the database session in a `finally` block or context manager?**
> Closing the database session returns the connection back to the database connection pool. If you don't close sessions, connections will remain open, causing a connection leak that will eventually make the database run out of available connections and crash.

**Q7. Explain the `yield` statement in the `get_db` dependency.**
> The `yield` statement returns a database session to the route function when requested. Once the route finishes executing and returns a response, FastAPI automatically resumes executing the code after `yield` (in the `finally` block), which ensures the session gets closed safely.

**Q8. What are the main benefits of using SQLAlchemy ORM over raw SQL?**
> 1. Database Portability: You can switch from SQLite to PostgreSQL by simply updating the database URL. 2. Safety: It automatically protects against SQL injection attacks. 3. Pythonic syntax: It provides auto-complete support, type safety, and lets you avoid writing strings of SQL manually.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
