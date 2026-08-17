from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Basic Routes

@app.get("/")
def home():
    return {
        "message": "Welcome to the Home Route"
    }


@app.get("/about")
def about():
    return {
        "message": "This is the About Route"
    }


@app.get("/contact")
def contact():
    return {
        "message": "Contact us at hello@example.com"
    }


# Path Parameters


# fixed route must come before dynamic route

@app.get("/users/me")
def get_current_user():
    return {
        "user": "current logged-in user"
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
        }


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": f"Item number {item_id}"}


# Query Parameters


@app.get("/products")
def get_products(
    category: str,
    limit: int = 10,
    page: int = 1,
    search: Optional[str] = None
):
    return {
        "category": category,
        "limit": limit,
        "page": page,
        "search": search
    }


# Path + Query Parameters Combined

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
