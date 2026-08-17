# 📌 Module 2 — API Routes, Path Parameters & Query Parameters

---

## 🛣️ What are Routes?

A **route** (also called an endpoint) is a URL path that your API listens on. When a client sends a request to that path, your function runs and returns a response.

```python
@app.get("/users")
def get_users():
    return {"users": []}
```

Routes in FastAPI use Python **decorators** — the decorator defines the HTTP method and path, and the function below it handles the request.

---

## 🔀 HTTP Methods in FastAPI

| Decorator         | HTTP Method | Use Case                  |
|-------------------|-------------|---------------------------|
| `@app.get()`      | GET         | Fetch / read data         |
| `@app.post()`     | POST        | Create new data           |
| `@app.put()`      | PUT         | Update existing data      |
| `@app.patch()`    | PATCH       | Partial update            |
| `@app.delete()`   | DELETE      | Delete data               |

---

## 🗺️ Creating Multiple Routes

You can define as many routes as you need. FastAPI matches them **top to bottom** — order matters!

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Home Route"}

@app.get("/about")
def about():
    return {"message": "This is the About Route"}

@app.get("/contact")
def contact():
    return {"message": "Contact us at hello@example.com"}
```

---

## 🔑 Path Parameters (Dynamic Routes)

Path parameters let you capture a **variable value from the URL**.

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

How it works:
- Use `{variable_name}` in the path with curly braces
- Declare the same name as a **function parameter**
- Add a **type hint** (`int`, `str`, etc.) — FastAPI validates & converts automatically

### Type Validation Example:
```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```
- `GET /items/5` → ✅ returns `{"item_id": 5}`
- `GET /items/abc` → ❌ FastAPI auto-returns `422 Unprocessable Entity`

---

## ⚠️ Route Order Matters — Fixed vs Dynamic

If you have a **fixed route** and a **dynamic route** that could conflict, always put the **fixed route first**:

```python
# ✅ Correct order
@app.get("/users/me")        # fixed — must come FIRST
def get_current_user():
    return {"user": "current logged-in user"}

@app.get("/users/{user_id}") # dynamic — comes AFTER
def get_user(user_id: int):
    return {"user_id": user_id}
```

If you reverse the order, `/users/me` would be captured by `{user_id}` and fail validation since `"me"` is not an `int`.

---

## ❓ Query Parameters

Query parameters are the **key=value pairs after `?` in a URL**.

```
GET /products?category=shoes&limit=10&page=2
```

In FastAPI, any function parameter **not** in the path is automatically treated as a query parameter:

```python
@app.get("/products")
def get_products(category: str, limit: int, page: int):
    return {
        "category": category,
        "limit": limit,
        "page": page
    }
```

Call it with: `GET /products?category=shoes&limit=10&page=2`

---

## 🎯 Optional Query Parameters

Make a parameter optional by giving it a **default value**:

```python
from typing import Optional

@app.get("/products")
def get_products(
    category: str,
    limit: int = 10,       # default = 10
    page: int = 1,         # default = 1
    search: Optional[str] = None   # fully optional
):
    return {
        "category": category,
        "limit": limit,
        "page": page,
        "search": search
    }
```

| Call | Result |
|------|--------|
| `/products?category=shoes` | `limit=10, page=1, search=None` |
| `/products?category=shoes&limit=5` | `limit=5, page=1, search=None` |
| `/products?category=shoes&search=nike` | `limit=10, page=1, search="nike"` |

> **Note:** In Python 3.10+, you can write `str | None = None` instead of `Optional[str] = None`. Both work.

---

## 🔀 Combining Path + Query Parameters

You can mix both freely — FastAPI figures out which is which automatically:

```python
@app.get("/users/{user_id}/posts")
def get_user_posts(
    user_id: int,           # path parameter
    limit: int = 5,         # query parameter
    published: bool = True  # query parameter
):
    return {
        "user_id": user_id,
        "limit": limit,
        "published": published
    }
```

Call: `GET /users/42/posts?limit=3&published=false`

---

## 📁 Files in This Folder

```
2_routes_and_params/
├── README.md           ← You are here (theory + concepts)
├── main.py             ← All route examples in one file
├── path_params.py      ← Path parameter examples
└── query_params.py     ← Query parameter examples
```

---

## ▶️ How to Run

```bash
# Navigate to this folder
cd 2_routes_and_params

# Run the server
uvicorn main:app --reload

# Open in browser
# http://127.0.0.1:8000/docs  ← Swagger UI (test all routes here)
```

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
