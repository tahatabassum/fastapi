# 📌 Module 15 — CORS & Environment Variables

This module covers two essential production topics:
1. **CORS (Cross-Origin Resource Sharing):** Allowing front-end apps (React, Vue, etc.) running on different domains to talk to your FastAPI backend.
2. **Environment Variables:** Storing sensitive settings (like API keys and DB credentials) securely outside your codebase using a `.env` file.

---

## 🌐 What is CORS?

By default, web browsers block frontend scripts from making requests to an API running on a different domain/port. This security policy is called **Same-Origin Policy**.

If your React app runs on `http://localhost:3000` and your FastAPI backend runs on `http://localhost:8000`, the browser will block the API requests unless the backend explicitly allows it.

### 🛡️ Adding CORSMiddleware in FastAPI

FastAPI includes a built-in `CORSMiddleware` to handle this easily:

```python
from fastapi.middleware.cors import CORSMiddleware

# Define which origins/domains are allowed to make requests
origins = [
    "http://localhost:3000",
    "https://myfrontendapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allowed origins
    allow_credentials=True,           # Support cookies/auth headers
    allow_methods=["*"],              # Allowed HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allowed HTTP headers
)
```

---

## 🔑 Environment Variables & `.env`

It is dangerous to hardcode credentials (like database passwords or JWT secrets) directly in your code. If you push your code to GitHub, anyone can see them.

Instead, we use a `.env` file to store them as key-value pairs:

```env
DATABASE_URL=sqlite:///./prod.db
SECRET_KEY=my-super-secret-key-123
DEBUG=True
```

### ⚙️ Reading `.env` in Python

We install `python-dotenv` to read these variables into our Python app:

```python
import os
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

# Access them using os.getenv()
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

> ⚠️ **Crucial Security Rule:** Never commit your `.env` file to GitHub! Our `.gitignore` is already set up to exclude `.env` files. Instead, developers commit a `.env.example` showing the names of keys without the actual secret values.

---

## 📁 Folder Structure

```
15_cors_env/
├── README.md       ← You are here
├── main.py         ← FastAPI app with CORS and Env loading
└── .env            ← Local secret configuration (git-ignored)
```

---

## ▶️ How to Run

Install dependencies:
```bash
pip install python-dotenv
```

Run the server:
```bash
cd 15_cors_env
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

## 🎯 Interview Questions

**Q1. What is CORS and why do browsers enforce it?**
> CORS stands for Cross-Origin Resource Sharing. It is a security mechanism enforced by web browsers to restrict web pages from making requests to a different domain than the one that served the web page. It prevents malicious sites from executing unauthorized requests against your API.

**Q2. What is an "Origin" in the context of web requests?**
> An origin is defined by the combination of the **Protocol** (HTTP/HTTPS), the **Domain/Host** (localhost/example.com), and the **Port** (8000/3000). If any of these three elements differ between the frontend and the backend, the request is considered cross-origin.

**Q3. How do you configure CORS in a FastAPI application?**
> You use `CORSMiddleware` from `fastapi.middleware.cors`. You specify a list of allowed origins under `allow_origins`, and add it to the application middleware chain using `app.add_middleware()`.

**Q4. What is the danger of setting `allow_origins=["*"]` in production?**
> Setting `"*" ` allows any website on the internet to make requests to your API. While useful for public APIs, it exposes private APIs to CSRF (Cross-Site Request Forgery) attacks and unauthorized cross-domain access.

**Q5. Why should you store database credentials and API keys in environment variables?**
> Storing credentials in environment variables keeps sensitive data out of source control. This prevents credentials from being exposed on public repositories (like GitHub) and allows different environments (development, staging, production) to use different configurations easily.

**Q6. What does `load_dotenv()` from `python-dotenv` do?**
> It reads key-value pairs from a `.env` file in the project root directory and loads them into Python's environment dictionary (`os.environ`). You can then access them using `os.getenv()`.

**Q7. What is a `.env.example` file?**
> A `.env.example` is a placeholder file committed to Git that lists all the required configuration keys (e.g., `DATABASE_URL=`, `SECRET_KEY=`) without the actual sensitive values. It serves as a guide for other developers setting up the project locally.

**Q8. What happens if `os.getenv("SECRET_KEY")` is called but the key doesn't exist in the `.env` file?**
> It returns `None` by default without throwing an error. You can provide a fallback value like `os.getenv("SECRET_KEY", "default_value")` or explicitly raise an error if the key is mandatory.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
