# 📌 Module 8 — Dependency Injection

---

## 🧠 What is Dependency Injection?

**Dependency Injection (DI)** means providing a function with the things it needs (dependencies) automatically — instead of creating them inside the function manually.

In FastAPI, DI is done using `Depends()`.

---

## ⚙️ What is `Depends()`?

`Depends()` tells FastAPI: **"Before running this route, run this function first and pass its result in."**

```python
from fastapi import Depends

def get_db():
    return {"db": "connected"}

@app.get("/items")
def get_items(db = Depends(get_db)):
    return db
```

FastAPI calls `get_db()` automatically before `get_items()` runs, and injects the result as `db`.

---

## ♻️ Reusable Logic with Dependencies

The real power of DI is **reusing the same logic across multiple routes** without repeating code.

### Without DI (repeated code):
```python
@app.get("/users")
def get_users(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### With DI (clean & reusable):
```python
def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/users")
def get_users(params = Depends(pagination)):
    return params

@app.get("/items")
def get_items(params = Depends(pagination)):
    return params
```

Now both routes share the same pagination logic. Change it in one place, it updates everywhere.

---

## 🔒 Auth Example with DI

A common use case — checking an API key before allowing access to a route:

```python
from fastapi import Header, HTTPException

def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return x_token

@app.get("/secure-data")
def secure_route(token = Depends(verify_token)):
    return {"message": "Access granted", "token": token}
```

Now every route that uses `Depends(verify_token)` is protected — no need to repeat the auth check in each route.

---

## 📦 Multiple Dependencies

A route can have multiple dependencies:

```python
@app.get("/dashboard")
def dashboard(
    params = Depends(pagination),
    token = Depends(verify_token)
):
    return {"params": params, "token": token}
```

---

## 📁 Files in This Folder

```
8_dependency_injection/
├── README.md   ← You are here
└── main.py     ← All examples in one runnable file
```

---

## ▶️ How to Run

```bash
cd 8_dependency_injection
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

## 🎯 Interview Questions

**Q1. What is Dependency Injection and why is it useful?**
> Dependency Injection is a pattern where a function receives what it needs from the outside instead of creating it internally. In FastAPI, it avoids code repetition — shared logic like auth checks, DB connections, or pagination is written once and reused across many routes.

**Q2. What is `Depends()` in FastAPI?**
> `Depends()` is FastAPI's built-in tool for dependency injection. You pass a function to it, and FastAPI automatically calls that function and injects its return value into your route. Example: `def get_items(db = Depends(get_db))`.

**Q3. When does FastAPI execute the dependency function?**
> FastAPI executes the dependency function **before** running the route function. The result is then passed as a parameter into the route.

**Q4. Can a dependency function have its own parameters?**
> Yes. A dependency function can have path params, query params, headers, or even other dependencies. FastAPI handles all of them automatically, just like a normal route function.

**Q5. Can one route have multiple dependencies?**
> Yes. You can add multiple `Depends()` calls in a single route's parameters. FastAPI runs all of them before executing the route function.

**Q6. What is a common real-world use case for `Depends()`?**
> The most common use cases are: authentication (verify a token before allowing access), database session management (create and close a DB session per request), and shared query parameters like pagination (`skip`, `limit`).

**Q7. What is the difference between a regular function and a dependency?**
> Any regular Python function can be a dependency — there's nothing special about it. What makes it a dependency is using `Depends(function_name)` in a route's parameters. FastAPI then treats it as something to resolve before the route runs.

**Q8. Can dependencies be nested (a dependency that uses another dependency)?**
> Yes. A dependency function can itself use `Depends()` to depend on another function. FastAPI resolves the entire chain automatically before the route runs.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
