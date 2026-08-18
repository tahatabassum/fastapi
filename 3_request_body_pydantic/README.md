# 📌 Module 3 — Request Body & Pydantic Validation

---

## 📦 What is a Request Body?

When you send a `POST`, `PUT`, or `PATCH` request, you often need to send **data along with the request** — not in the URL, but in the **body** of the request.

For example, creating a new user:
```
POST /users
Body: { "name": "Taha", "email": "taha@example.com", "age": 22 }
```

In FastAPI, you define the shape of that body using a **Pydantic model**.

---

## 🧩 What is Pydantic?

**Pydantic** is a Python library for data **validation and parsing** using type hints.

FastAPI uses Pydantic under the hood to:
- ✅ Validate incoming request data
- ✅ Convert data types automatically (`"22"` → `22`)
- ✅ Return clear error messages if data is wrong
- ✅ Auto-generate schema in Swagger docs

---

## 🏗️ Defining a Pydantic Model

You create a class that inherits from `BaseModel`:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
```

Each field has a **name** and a **type**. That's it — Pydantic handles the rest.

---

## 📬 Using the Model in a POST Route

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "user": user
    }
```

FastAPI sees that `user` is a `BaseModel` type → treats it as the **request body**.

Send this JSON in the request:
```json
{
    "name": "Taha",
    "email": "taha@example.com",
    "age": 22
}
```

Response:
```json
{
    "message": "User created successfully",
    "user": {
        "name": "Taha",
        "email": "taha@example.com",
        "age": 22
    }
}
```

---

## 🎯 Optional Fields & Default Values

You can make fields optional by giving them a **default value**:

```python
from typing import Optional

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None   # optional, defaults to None
    in_stock: bool = True               # optional, defaults to True
```

| Field | Required? | Default |
|---|---|---|
| `name` | ✅ Required | — |
| `price` | ✅ Required | — |
| `description` | ❌ Optional | `None` |
| `in_stock` | ❌ Optional | `True` |

---

## ✅ Built-in Validation with Pydantic

Pydantic validates data **automatically**. If wrong data is sent, FastAPI returns a `422 Unprocessable Entity` with a clear error message.

```python
class Item(BaseModel):
    name: str
    price: float
    quantity: int
```

| Sent Data | Result |
|---|---|
| `{"name": "Bag", "price": 9.99, "quantity": 2}` | ✅ 200 OK |
| `{"name": "Bag", "price": "nine", "quantity": 2}` | ❌ 422 — price must be float |
| `{"name": "Bag", "quantity": 2}` | ❌ 422 — price is required |
| `{"name": "Bag", "price": 9.99, "quantity": "two"}` | ❌ 422 — quantity must be int |

---

## 🔍 Field Validation with `Field()`

For more control over validation, use Pydantic's `Field()`:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, description="Price must be greater than 0")
    quantity: int = Field(ge=0, le=1000)
```

| Validator | Meaning |
|---|---|
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `gt` | Greater than |
| `ge` | Greater than or equal |
| `lt` | Less than |
| `le` | Less than or equal |
| `description` | Shows in Swagger docs |

---

## 🪆 Nested Models

A Pydantic model can contain **another Pydantic model** as a field:

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    email: str
    address: Address      # nested model
```

Send this JSON:
```json
{
    "name": "Taha",
    "email": "taha@example.com",
    "address": {
        "street": "123 Main St",
        "city": "Karachi",
        "country": "Pakistan"
    }
}
```

---

## 📋 Model with a List (Nested List)

```python
from typing import List

class Tag(BaseModel):
    name: str
    color: str

class BlogPost(BaseModel):
    title: str
    content: str
    tags: List[Tag]       # list of nested models
```

Send this JSON:
```json
{
    "title": "FastAPI Guide",
    "content": "FastAPI is awesome...",
    "tags": [
        {"name": "python", "color": "blue"},
        {"name": "fastapi", "color": "green"}
    ]
}
```

---

## 🔗 Request Body + Path + Query Together

You can combine all three in one route:

```python
@app.put("/items/{item_id}")
def update_item(
    item_id: int,              # path parameter
    in_stock: bool = True,     # query parameter
    item: Item                 # request body
):
    return {
        "item_id": item_id,
        "in_stock": in_stock,
        "item": item
    }
```

FastAPI automatically knows:
- `item_id` → **path** (it's in the URL)
- `in_stock` → **query** (it's a simple type, not in path)
- `item` → **body** (it's a Pydantic model)

---

## 📁 Files in This Folder

```
3_request_body_pydantic/
├── README.md       ← You are here (theory + concepts)
└── main.py         ← All examples in one runnable file
```

---

## ▶️ How to Run

```bash
cd 3_request_body_pydantic
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

> **Tip:** Use Swagger UI at `/docs` to test POST requests directly — no Postman needed!

---

## 🎯 Interview Questions

**Q1. What is a request body and when do you use it?**
> A request body is data sent by the client inside the HTTP request (not in the URL). You use it with `POST`, `PUT`, and `PATCH` requests — for example, when creating or updating a resource with multiple fields.

**Q2. What is Pydantic and what role does it play in FastAPI?**
> Pydantic is a Python data validation library. In FastAPI, you define request/response schemas as Pydantic `BaseModel` classes. FastAPI uses them to automatically validate incoming data, convert types, and generate Swagger documentation.

**Q3. How does FastAPI know a function parameter is a request body?**
> If a function parameter's type is a Pydantic `BaseModel` subclass, FastAPI automatically treats it as the request body. Simple types like `int` or `str` become path or query params.

**Q4. What happens if required field is missing in the request body?**
> FastAPI returns a `422 Unprocessable Entity` error with a detailed message specifying which field is missing. This validation happens automatically via Pydantic before your function even runs.

**Q5. How do you make a field optional in a Pydantic model?**
> Give it a default value. Use `field: Optional[str] = None` to allow `None`, or `field: str = "default"` for a specific default. Fields without defaults are required.

**Q6. What is `Field()` in Pydantic and why use it?**
> `Field()` adds extra validation and metadata to a model field. For example: `price: float = Field(gt=0)` ensures price is greater than 0. You can also add `min_length`, `max_length`, `le`, `ge`, and `description` for Swagger docs.

**Q7. What are nested Pydantic models?**
> A Pydantic model can use another Pydantic model as a field type. This allows you to represent complex structured data like a `User` that contains an `Address` object. FastAPI handles validation for all nested levels automatically.

**Q8. Can you combine a request body with path and query parameters in one route?**
> Yes. FastAPI distinguishes them automatically: path params match `{}` in the URL, query params are simple types not in the path, and the request body is a Pydantic model. All three can exist in a single route function.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
