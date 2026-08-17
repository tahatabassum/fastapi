from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


# Input model - what client sends (includes password)
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# Response model - what client receives (no password)
class UserResponse(BaseModel):
    name: str
    email: str


# Fake in-memory DB
fake_users_db = [
    {"name": "Taha", "email": "taha@example.com", "password": "secret123"},
    {"name": "Ali",  "email": "ali@example.com",  "password": "pass456"},
]


# Create user - password is hidden in response
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    fake_users_db.append(user.model_dump())
    return user


# Get all users - list response model
@app.get("/users", response_model=List[UserResponse])
def get_users():
    return fake_users_db


# Get one user by index
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id >= len(fake_users_db):
        raise HTTPException(status_code=404, detail="User not found")
    return fake_users_db[user_id]


# Exclude email field from response
@app.get("/users/{user_id}/name-only", response_model=UserResponse, response_model_include={"name"})
def get_user_name(user_id: int):
    if user_id >= len(fake_users_db):
        raise HTTPException(status_code=404, detail="User not found")
    return fake_users_db[user_id]


# Optional field example
class UserProfile(BaseModel):
    name: str
    bio: Optional[str] = None
    website: Optional[str] = None


# Exclude None fields from response
@app.get("/profile", response_model=UserProfile, response_model_exclude_none=True)
def get_profile():
    return {"name": "Taha", "bio": None, "website": None}
