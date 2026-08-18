# 📌 Module 7 — Exception Handling

---

## 🧠 What is Exception Handling?

Exception handling is the process of responding to errors in a controlled way. Instead of crashing the app, you catch the error and return a meaningful response to the client.

FastAPI gives you three ways to handle exceptions:
1. **`HTTPException`** — simple built-in way (covered in module 6)
2. **Custom exceptions** — your own exception classes
3. **Global error handlers** — catch exceptions app-wide

---

## 1️⃣ HTTPException (Quick Recap)

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Item not found")
```

Simple and works for most cases. But if you want reusable, descriptive errors — use custom exceptions.

---

## 2️⃣ Custom Exceptions

Create your own exception class by inheriting from Python's built-in `Exception`:

```python
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
```

Then raise it like any Python exception:

```python
raise ItemNotFoundError(item_id=5)
```

By itself, this would cause a `500 Internal Server Error`. That's why you pair it with a **handler**.

---

## 3️⃣ Global Error Handlers

A global handler tells FastAPI: **"Whenever this exception is raised anywhere in the app, run this function"**.

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Item {exc.item_id} does not exist"}
    )
```

Now whenever `ItemNotFoundError` is raised, FastAPI catches it and returns a clean `404` response automatically — no try/except needed in each route.

---

## ✅ Why Use Custom Exceptions + Global Handlers?

| Approach | Code Repetition | Reusability | Readability |
|----------|----------------|-------------|-------------|
| `HTTPException` in each route | High | Low | Medium |
| Custom exception + global handler | Low | High | High |

In small projects, `HTTPException` is fine. In larger apps, custom exceptions keep your routes clean.

---

## 🔁 Full Flow Example

```python
# 1. Define custom exception
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

# 2. Register global handler
@app.exception_handler(ItemNotFoundError)
async def handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Item {exc.item_id} does not exist"}
    )

# 3. Raise it in routes — handler catches it automatically
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise ItemNotFoundError(item_id=item_id)
    return items[item_id]
```

---

## 📁 Files in This Folder

```
7_exception_handling/
├── README.md   ← You are here
└── main.py     ← All examples in one runnable file
```

---

## ▶️ How to Run

```bash
cd 7_exception_handling
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

## 🎯 Interview Questions

**Q1. What are the three ways to handle exceptions in FastAPI?**
> 1. `HTTPException` — built-in, simple, raise it directly in routes. 2. Custom exception classes — define your own errors with descriptive names. 3. Global exception handlers — registered with `@app.exception_handler()`, catches a specific exception type across the entire app.

**Q2. What is a custom exception in Python/FastAPI?**
> A custom exception is a class that inherits from Python's `Exception`. You define it to represent a specific error with its own data. For example, `ItemNotFoundError` stores the `item_id` so the handler can use it in the error message.

**Q3. What happens if you raise a custom exception without a handler?**
> FastAPI doesn't know how to handle it and returns a `500 Internal Server Error`. Always pair a custom exception with a `@app.exception_handler()` or catch it manually.

**Q4. How does `@app.exception_handler()` work?**
> It registers a function that FastAPI calls automatically whenever a specific exception type is raised anywhere in the app. The function receives the `request` and the `exc` (exception object) and returns a response.

**Q5. What is the difference between `HTTPException` and a custom exception?**
> `HTTPException` is FastAPI's built-in exception that directly maps to an HTTP response. A custom exception is a plain Python exception — you need a handler to convert it to an HTTP response. Custom exceptions are more descriptive and reusable across large apps.

**Q6. Why is `async def` used in exception handlers?**
> Exception handlers in FastAPI are ASGI middleware-level functions that need to be async to work with FastAPI's async request/response cycle. Using `async def` allows them to handle async operations without blocking.

**Q7. Can you have multiple global exception handlers in one app?**
> Yes. You can register a separate `@app.exception_handler()` for each exception type. Each one handles only its specific exception type.

**Q8. When should you use a global handler vs `HTTPException` in each route?**
> Use `HTTPException` for simple, one-off errors in small projects. Use global handlers when the same error type occurs in multiple routes — it avoids repetition and keeps route functions clean and focused.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
