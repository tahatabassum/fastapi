# 📌 Module 1 — Introduction to FastAPI

---

## 🧠 What is an API?

An **API (Application Programming Interface)** is a set of rules that allows different software applications to communicate with each other.

Think of it like a **waiter in a restaurant**:
- You (client) place an order
- The waiter (API) carries the request to the kitchen (server)
- The kitchen prepares the food and returns it through the waiter

In web development, APIs typically follow the **REST** (Representational State Transfer) pattern, where the client sends HTTP requests and the server responds with data (usually JSON).

### Common HTTP Methods:
| Method   | Purpose              |
|----------|----------------------|
| `GET`    | Retrieve data        |
| `POST`   | Create new data      |
| `PUT`    | Update existing data |
| `DELETE` | Remove data          |
| `PATCH`  | Partial update       |

---

## ⚡ What is FastAPI?

**FastAPI** is a modern, high-performance web framework for building APIs with **Python 3.7+** based on standard Python type hints.

It was created by **Sebastián Ramírez** and first released in **2018**.

### Key Characteristics:
- Built on top of **Starlette** (ASGI framework) and **Pydantic** (data validation)
- Uses **Python type hints** for request/response validation
- Generates **automatic interactive documentation** (Swagger UI & ReDoc)
- Supports **async/await** natively (non-blocking I/O)

---

## 🚀 Why FastAPI?

| Feature                         | Details                                                                 |
|---------------------------------|-------------------------------------------------------------------------|
| ⚡ **High Performance**          | One of the fastest Python frameworks available                          |
| 🔍 **Automatic Docs**           | Swagger UI at `/docs`, ReDoc at `/redoc` — generated automatically      |
| ✅ **Built-in Validation**      | Request & response validation via Pydantic — no extra libraries needed  |
| 🔒 **Type Safety**              | Python type hints enforce correct data types at runtime                 |
| 🧩 **Dependency Injection**     | Clean, reusable logic via built-in DI system                            |
| 🔄 **Async Support**            | First-class `async`/`await` support for high concurrency                |
| 📦 **Standards-Based**          | Based on OpenAPI & JSON Schema standards                                |
| 🛠️ **Developer Friendly**       | Less boilerplate, faster development, editor autocomplete support       |

---

## ⚖️ FastAPI vs Flask vs Django

| Feature                  | FastAPI              | Flask                  | Django                      |
|--------------------------|----------------------|------------------------|-----------------------------|
| **Type**                 | API framework        | Micro framework        | Full-stack framework        |
| **Performance**          | ⚡ Very High          | 🐢 Moderate             | 🐢 Moderate                  |
| **Auto Docs**            | ✅ Built-in           | ❌ Needs extension      | ❌ Needs DRF + extension     |
| **Data Validation**      | ✅ Pydantic built-in  | ❌ Manual / extensions  | ✅ Django Forms / Serializers|
| **Async Support**        | ✅ Native             | ⚠️ Limited (Flask 2.0) | ⚠️ Limited                  |
| **ORM**                  | ❌ Bring your own     | ❌ Bring your own       | ✅ Django ORM built-in       |
| **Learning Curve**       | 📘 Easy–Medium        | 📗 Easy                 | 📕 Steep                     |
| **Best For**             | REST APIs, microservices | Simple apps, APIs   | Full web apps, admin panels |


---

## 🛠️ Setup & Installation

### Prerequisites:
- Python 3.7+ installed
- `pip` package manager

### Check Python Version:
```bash
python --version
# or
python3 --version
```

### Option 1: Global Installation
```bash
pip install fastapi uvicorn
```

### Option 2: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn
```

> **Why venv?** Just like `node_modules` is scoped to a project in Node.js, a virtual environment keeps your Python dependencies isolated per project — avoiding version conflicts.

---

## 👋 Hello World API

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
```

### Run the server:
```bash
uvicorn main:app --reload
```

> `uvicorn` is the ASGI server for FastAPI — similar to how you'd use `node index.js` or `nodemon` in Express.

| Flag       | Meaning                                      |
|------------|----------------------------------------------|
| `main`     | The Python file name (`main.py`)             |
| `app`      | The FastAPI instance inside that file        |
| `--reload` | Auto-restart on file changes (like nodemon)  |

### Visit:
- `http://127.0.0.1:8000` → Your API
- `http://127.0.0.1:8000/docs` → **Swagger UI** (interactive docs)
- `http://127.0.0.1:8000/redoc` → **ReDoc** (alternative docs)

---

## 📚 Automatic API Documentation (Swagger UI)

One of FastAPI's killer features — **zero-config interactive API docs**.

When you run your FastAPI app, it automatically generates:

### Swagger UI (`/docs`)
- Fully interactive — test endpoints directly in the browser
- Shows request/response schemas
- Equivalent to Postman, but built right in

### ReDoc (`/redoc`)
- Cleaner, read-only documentation view
- Great for sharing API docs externally

These are generated from the **OpenAPI specification** that FastAPI builds automatically from your code.

---

## 🗺️ Full Course Roadmap

### 📦 Session 1 — Basics + CRUD (`00:00 – 01:33`)
| Module | Topic |
|--------|-------|
| `1_intro` | Intro, What is API/FastAPI, Setup |
| `2_routes_and_params` | Routes, Path Params, Query Params |
| `3_request_body_pydantic` | Request Body, Pydantic Models, Nested Models |
| `4_todo_crud` | CRUD To-Do Project (GET, POST, PUT, DELETE) |
| `5_response_models` | Response Models, Hiding Sensitive Data |

### 🗄️ Session 2 — DB + Auth (`01:33 – 03:48`)
| Module | Topic |
|--------|-------|
| `6_status_codes_errors` | Status Codes, Custom Responses, Exception Handling |
| `7_dependency_injection` | Dependency Injection & Reusable Logic |
| `8_middleware` | Middleware |
| `9_database_sqlalchemy` | DB Integration, SQLAlchemy ORM |
| `10_crud_with_db` | CRUD API with Database |
| `11_async_await` | Asynchronous Programming |
| `12_auth_jwt` | JWT Auth, OAuth2, Password Hashing |
| `13_file_uploads` | File Uploads & Static Files |

### 🚀 Session 3 — Production + Project (`03:48 – 05:01`)
| Module | Topic |
|--------|-------|
| `14_cors_env` | CORS Handling & Environment Variables |
| `15_testing_pytest` | API Testing with Pytest |
| `16_third_party_webcrawling` | Third-Party API Integration & Web Crawling |
| `17_pagination_caching_ratelimit` | Pagination, Caching, Rate Limiting |
| `18_deployment` | Deploying to Render |
| `19_blog_api_project` | Real-World Blog API Project |

---

## 🔑 Key Concepts Introduced Here

- ✅ FastAPI is built on Starlette (ASGI) + Pydantic
- ✅ Uses Python decorators for routing (`@app.get`, `@app.post`, etc.)
- ✅ Auto-generates Swagger docs with zero config
- ✅ Virtual environments keep dependencies isolated
- ✅ `uvicorn` is the dev server (like nodemon for Python)

---

## 📁 What's in This Folder

```
1_intro/
└── README.md        ← You are here (theory + concepts)
```

> **Note:** This is a theory module. No code files are needed here — all concepts are explained above. Hands-on coding starts from `2_routes_and_params`.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
