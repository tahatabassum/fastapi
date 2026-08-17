# 📌 Module 4 — CRUD To-Do API Project

---

## 🧠 What is CRUD?

**CRUD** stands for the four basic operations you perform on data:

| Operation | HTTP Method | Action |
|-----------|-------------|--------|
| **C**reate | `POST` | Add a new item |
| **R**ead | `GET` | Fetch one or all items |
| **U**pdate | `PUT` | Replace/update an item |
| **D**elete | `DELETE` | Remove an item |

This module builds a complete **To-Do List API** using all four operations with in-memory storage (a Python dictionary).

---

## 📋 The Todo Model

```python
class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
```

- `title` — required
- `description` — optional, defaults to `None`
- `completed` — defaults to `False`

---

## 🗄️ In-Memory Storage

```python
todos = {}
counter = 1
```

No database yet — todos are stored in a dictionary with an auto-incrementing integer as the key (ID).

---

## CREATE — `POST /todos`

```python
@app.post("/todos")
def create_todo(todo: Todo):
    global counter
    todos[counter] = todo
    counter += 1
    return {"id": counter - 1, "todo": todo}
```

**Request body:**
```json
{
    "title": "Learn FastAPI",
    "description": "Complete the CRUD module",
    "completed": false
}
```

---

## READ ALL — `GET /todos`

```python
@app.get("/todos")
def get_todos():
    return todos
```

Returns all todos stored in the dictionary.

---

## READ ONE — `GET /todos/{todo_id}`

```python
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]
```

Returns a single todo by ID. Raises `404` if not found.

---

## UPDATE — `PUT /todos/{todo_id}`

```python
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = todo
    return {"message": "Todo updated", "todo": todo}
```

Replaces the existing todo with new data.

---

## DELETE — `DELETE /todos/{todo_id}`

```python
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(todo_id)
    return {"message": "Todo deleted"}
```

Removes the todo from the dictionary.

---

## ⚠️ HTTPException

Used to return proper HTTP error responses when something goes wrong:

```python
raise HTTPException(status_code=404, detail="Todo not found")
```

Returns:
```json
{
    "detail": "Todo not found"
}
```

| Status Code | Meaning |
|---|---|
| `200` | OK |
| `404` | Not Found |
| `422` | Validation Error |

---

## 🔁 API Summary

| Method | Endpoint | Action |
|--------|----------|--------|
| `POST` | `/todos` | Create a todo |
| `GET` | `/todos` | Get all todos |
| `GET` | `/todos/{id}` | Get one todo |
| `PUT` | `/todos/{id}` | Update a todo |
| `DELETE` | `/todos/{id}` | Delete a todo |

---

## ▶️ How to Run

```bash
cd 4_todo_crud
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
