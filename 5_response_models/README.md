# 📌 Module 5 — Response Models & Hiding Sensitive Data

---

## 🧠 What is a Response Model?

By default, FastAPI returns **everything** in your object. But sometimes you want to:
- Hide **sensitive fields** like passwords, tokens, internal IDs
- Control **exactly what the client sees**
- Ensure the response always has a **consistent shape**

FastAPI lets you define a separate **response model** using `response_model=` in the route decorator.

---

## ❌ The Problem — Returning Sensitive Data

```python
class User(BaseModel):
    name: str
    email: str
    password: str   # you don't want this in the response!
```

If you return the full `User` object, the password goes to the client — a big security issue.

---

## ✅ The Fix — Separate Response Model

Create two models: one for **input** (with password) and one for **output** (without password):

```python
# Input model — what the client sends
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# Response model — what the client receives
class UserResponse(BaseModel):
    name: str
    email: str
```

Then use `response_model` in the route:

```python
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return user  # FastAPI filters out 'password' automatically
```

Even though `user` has a `password` field, FastAPI only returns fields defined in `UserResponse`.

---

## 🔢 Response Model for Lists

To return a list of items, wrap it with `List[]`:

```python
from typing import List

@app.get("/users", response_model=List[UserResponse])
def get_users():
    return fake_users_db
```

---

## 🚫 Excluding Fields with `response_model_exclude`

You can also exclude specific fields without creating a separate model:

```python
@app.get("/users/{user_id}", response_model=UserResponse, response_model_exclude={"email"})
def get_user(user_id: int):
    return fake_users_db[user_id]
```

---

## ✅ Including Only Specific Fields with `response_model_include`

```python
@app.get("/users/{user_id}", response_model=UserResponse, response_model_include={"name"})
def get_user(user_id: int):
    return fake_users_db[user_id]
```

---

## 🎯 `response_model_exclude_none`

By default, optional fields with `None` value are still included in the response. Use `response_model_exclude_none=True` to hide them:

```python
@app.get("/users/{user_id}", response_model=UserResponse, response_model_exclude_none=True)
def get_user(user_id: int):
    return fake_users_db[user_id]
```

---

## 📁 Files in This Folder

```
5_response_models/
├── README.md   ← You are here
└── main.py     ← All response model examples
```

---

## ▶️ How to Run

```bash
cd 5_response_models
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
