# 📌 Module 11 — CRUD with Database

---

## 🧠 What is Database CRUD?

In this module, we transition from using in-memory storage (from Module 4) to executing persistent **CRUD (Create, Read, Update, Delete)** operations on a real **SQLite Database** using **SQLAlchemy ORM**.

---

## ⚙️ Complete CRUD Operations

### 1️⃣ Database Setup & Model
Before executing CRUD operations, we initialize the database engine, create a session generator, and define our table structure.

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(String, default="False") # Storing string representation "True"/"False" as shown in slides
```

---

### 2️⃣ Create Operation (Insert)
Inserts a new Todo record into the database.

```python
@app.post("/todos")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title=title, completed="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        "message": "Todo Created",
        "data": todo
    }
```

---

### 3️⃣ Read Operations (Select)
Fetches records from the database.

* **Read All:**
```python
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()
```

* **Read One:**
```python
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
```

---

### 4️⃣ Update Operation (Update)
Modifies an existing record.

```python
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str, completed: str, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = title
    todo.completed = completed
    db.commit()
    db.refresh(todo)
    return {
        "message": "Todo Updated",
        "data": todo
    }
```

---

### 5️⃣ Delete Operation (Delete)
Removes a record from the database.

```python
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {
        "message": "TODO Deleted"
    }
```

---

## 📁 Folder Structure

```
11_crud_with_db/
├── README.md   ← You are here
└── main.py     ← Full working CRUD API
```

---

## ▶️ How to Run

```bash
cd 11_crud_with_db
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

## 🎯 Interview Questions

**Q1. What is the purpose of `db.add(todo)` in SQLAlchemy?**
> `db.add(todo)` places the new model instance in the database session's "pending" state. It does not write to the database immediately; it prepares the object to be inserted during the next transaction flush or commit.

**Q2. What is the difference between `db.commit()` and `db.flush()`?**
> `db.flush()` sends individual SQL statements (like INSERT, UPDATE, DELETE) to the database transaction buffer without final approval. `db.commit()` writes all changes permanently to the database and ends the current transaction.

**Q3. What does `db.refresh(todo)` do?**
> `db.refresh(todo)` pulls the latest state of the object back from the database. This is useful because it updates the model instance with database-generated defaults, such as the auto-incremented primary key `id`.

**Q4. How do you query a single record by its ID using SQLAlchemy?**
> You query by calling `.filter(Model.id == target_id)` followed by `.first()`. For example: `db.query(Todo).filter(Todo.id == todo_id).first()`. Using `.first()` returns either the single model instance or `None` if not found.

**Q5. Why do we raise `HTTPException` if a query returns `None`?**
> If a requested item does not exist, SQL returns empty or `None`. Raising an `HTTPException(status_code=404)` ensures FastAPI returns a standard RESTful response code `404 Not Found` to the client instead of a generic `200 OK` with null values.

**Q6. What happens behind the scenes during `db.delete(todo)`?**
> SQLAlchemy schedules a DELETE SQL instruction for the target row in the database. The record is permanently removed from the table once `db.commit()` is called.

**Q7. Is it possible to perform updates without fetching the object first?**
> Yes. SQLAlchemy supports bulk updates directly on queries: `db.query(Todo).filter(Todo.id == todo_id).update({"title": new_title})`. However, fetching first and modifying attributes (as shown in the examples) is standard for simple objects.

**Q8. What happens to the database file `todos.db` when you write data?**
> SQLite creates/modifies a local binary database file named `todos.db`. The file persists on your drive, meaning even if your FastAPI application restarts or crashes, your data remains completely safe.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
