# 📌 Module 6 — Status Codes & Custom Responses

---

> **Note:** Basic `HTTPException` is covered here. For custom exceptions & global error handlers, see [Module 7 — Exception Handling](../7_exception_handling/).

## 📊 HTTP Status Codes

HTTP status codes are 3-digit numbers the server sends back to tell the client what happened.

| Code | Name | When to Use |
|------|------|-------------|
| `200` | OK | Default success response |
| `201` | Created | Resource successfully created (POST) |
| `204` | No Content | Success but nothing to return (DELETE) |
| `400` | Bad Request | Invalid input from client |
| `401` | Unauthorized | Not logged in |
| `403` | Forbidden | Logged in but no permission |
| `404` | Not Found | Resource doesn't exist |
| `422` | Unprocessable Entity | Validation error (FastAPI default) |
| `500` | Internal Server Error | Something crashed on the server |

---

## ✅ Setting Status Codes in FastAPI

By default FastAPI returns `200` for every successful response. You can change this using `status_code=` in the route decorator.

### Using raw numbers:
```python
@app.post("/items", status_code=201)
def create_item(item: Item):
    ...
```

### Using FastAPI's `status` module (recommended):
```python
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    ...
```

Using `status.HTTP_201_CREATED` is better than writing `201` — it's more readable and avoids typos.

---

## ⚠️ Error Handling with `HTTPException`

When something goes wrong, use `HTTPException` to return a proper error response:

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

This returns:
```json
{
    "detail": "Item not found"
}
```
With HTTP status `404 Not Found`.

---

## 📋 Full Code Summary

```python
# POST - 201 Created
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    ...

# GET - 200 OK
@app.get("/items", status_code=status.HTTP_200_OK)
def get_items():
    ...

# GET one - 404 if not found
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    ...

# DELETE - 204 No Content
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    ...
```

---

## 📁 Files in This Folder

```
6_status_codes_errors/
├── README.md   ← You are here
└── main.py     ← All examples in one runnable file
```

---

## ▶️ How to Run

```bash
cd 6_status_codes_errors
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

## 🎯 Interview Questions

**Q1. What are HTTP status codes and why are they important?**
> HTTP status codes are 3-digit numbers returned by the server to tell the client the result of their request. They follow a standard: `2xx` = success, `4xx` = client error, `5xx` = server error.

**Q2. What is the difference between `200`, `201`, and `204`?**
> `200 OK` is the default success response. `201 Created` is used when a new resource has been created (POST). `204 No Content` means success but nothing to return (DELETE).

**Q3. How do you set a custom status code for a route in FastAPI?**
> Pass `status_code=` to the route decorator: `@app.post("/items", status_code=201)`. Use `status.HTTP_201_CREATED` from FastAPI's `status` module for readability.

**Q4. What is `HTTPException` and when do you use it?**
> `HTTPException` is used to return an error response with a proper HTTP status code and message. You raise it when something goes wrong — like when a resource is not found.

**Q5. What is the difference between `401` and `403`?**
> `401 Unauthorized` means the user is not authenticated (not logged in). `403 Forbidden` means the user is logged in but doesn't have permission to access the resource.

**Q6. What status code does FastAPI return by default?**
> FastAPI returns `200 OK` by default for all successful responses unless you explicitly set a different `status_code` in the decorator.

**Q7. Why does the DELETE route return no body?**
> Because we use `status_code=204` (No Content). HTTP `204` means the action was successful but there's nothing to return. Adding a return value with `204` would be ignored.

**Q8. What status code does FastAPI return when Pydantic validation fails?**
> FastAPI automatically returns `422 Unprocessable Entity` with details about exactly which field failed validation.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
