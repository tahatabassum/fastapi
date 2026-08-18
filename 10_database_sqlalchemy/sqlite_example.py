import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

DB_FILE = "sqlite_test.db"

# Direct SQLite connection
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
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


class TodoCreate(BaseModel):
    title: str


@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    cursor.execute(
        "INSERT INTO todos (title, completed) VALUES (?, ?)", (todo.title, False)
    )
    conn.commit()
    todo_id = cursor.lastrowid
    return {"id": todo_id, "title": todo.title, "completed": False}


@app.get("/todos")
def get_todos():
    cursor.execute("SELECT id, title, completed FROM todos")
    rows = cursor.fetchall()
    # Format list of tuples into list of dicts
    todo_list = []
    for row in rows:
        todo_list.append({"id": row[0], "title": row[1], "completed": bool(row[2])})
    return todo_list
