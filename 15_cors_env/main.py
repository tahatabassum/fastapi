import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Read env variables
app_name = os.getenv("APP_NAME", "FastAPI App")
secret_key = os.getenv("SECRET_KEY", "default-fallback-secret")
database_url = os.getenv("DATABASE_URL", "sqlite:///./fallback.db")

# CORS Configurations
allowed_origins = [
    "http://localhost:3000",  # React default port
    "http://localhost:5173",  # Vite default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "app_name": app_name,
        "database_url": database_url,
        # Note: Do not return SECRET_KEY in real production response for security reasons!
        "secret_key_loaded": secret_key is not None,
    }
