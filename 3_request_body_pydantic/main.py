from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()


# Basic Pydantic Model

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


# Optional Fields & Default Values

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None  # optional
    in_stock: bool = True               # default True


@app.post("/products")
def create_product(product: Product):
    return {
        "message": "Product created",
        "product": product
    }


# Field Validation

class Item(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, description="Price must be greater than 0")
    quantity: int = Field(ge=0, le=1000)


@app.post("/items")
def create_item(item: Item):
    return {
        "message": "Item created",
        "item": item
    }


# Nested Models

class Address(BaseModel):
    street: str
    city: str
    country: str


class UserWithAddress(BaseModel):
    name: str
    email: str
    address: Address  # nested model


@app.post("/users/full")
def create_user_with_address(user: UserWithAddress):
    return {
        "message": "User with address created",
        "user": user
    }


# Nested List Model

class Tag(BaseModel):
    name: str
    color: str


class BlogPost(BaseModel):
    title: str
    content: str
    tags: List[Tag]  # list of nested models


@app.post("/posts")
def create_post(post: BlogPost):
    return {
        "message": "Blog post created",
        "post": post
    }


# Body + Path + Query Combined

@app.put("/items/{item_id}")
def update_item(
    item_id: int,           # path parameter
    in_stock: bool = True,  # query parameter
    item: Item = None       # request body
):
    return {
        "item_id": item_id,
        "in_stock": in_stock,
        "item": item
    }
