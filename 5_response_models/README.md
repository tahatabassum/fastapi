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

## 🎯 Interview Questions

**Q1. What is a response model in FastAPI?**
> A response model is a Pydantic model passed to the `response_model=` parameter in a route decorator. It controls exactly what data FastAPI returns to the client, filtering out any fields not defined in the response model.

**Q2. Why would you use a separate model for input and output?**
> To protect sensitive data. For example, a `UserCreate` model includes a `password` field for input, but the `UserResponse` model used for output doesn't — so the password is never returned to the client even if it's in the object you return.

**Q3. How does FastAPI filter response data using `response_model`?**
> FastAPI serializes the returned object using the response model's field definitions. Any field in the returned data that is not in the response model is automatically stripped from the response.

**Q4. What does `response_model_exclude_none=True` do?**
> It removes fields with `None` values from the response. Useful when you have optional fields that aren't set — instead of returning `{"bio": null, "website": null}`, they are simply omitted.

**Q5. What is `response_model_include` and `response_model_exclude`?**
> These let you include or exclude specific fields from the response without creating a new model. `response_model_include={"name"}` returns only the `name` field. `response_model_exclude={"email"}` returns everything except `email`.

**Q6. What happens if you return extra fields not in the response model?**
> FastAPI silently filters them out. The extra fields are never sent to the client. This is the core benefit — your internal data and external API response are cleanly separated.

**Q7. How do you define a response model for a list of items?**
> Wrap the model with `List[]` from `typing`: `response_model=List[UserResponse]`. FastAPI will validate and filter each item in the list against the model.

**Q8. Can you set a default HTTP status code for a route in FastAPI?**
> Yes, using the `status_code` parameter in the decorator: `@app.post("/users", status_code=201)`. This sets the response status code when the route succeeds.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
