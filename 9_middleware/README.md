# 📌 Module 9 — Middleware

---

## 🧠 What is Middleware?

**Middleware** is a function that runs before every request is processed by a route, and after every response is generated.

Think of it like a security guard standing at the door of your API. It can inspect incoming requests, modify them, measure execution time, or even reject them before they reach your path operations.

```
Incoming Request ──> [ Middleware ] ──> Route Handler (your code)
                                                │
Outgoing Response <── [ Middleware ] <──────────┘
```

---

## ⚙️ How Middleware Works (The HTTP Flow)

FastAPI allows you to register middleware by using the `@app.middleware("http")` decorator.

Every HTTP middleware function needs to accept:
1. `request`: The incoming `Request` object.
2. `call_next`: A function that receives the `request` and passes it to the corresponding route handler.

It must return the `response` received from `call_next`.

---

## ⏱️ Logging Middleware Example

A very common use case is measuring and logging how long each API request takes:

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    # 1. Runs before request reaches route
    start_time = time.time()
    
    # 2. Passes the request to the route handler
    response = await call_next(request)
    
    # 3. Runs after route handler returns response
    process_time = time.time() - start_time
    print(f"Path: {request.url.path} | Time: {process_time:.6f}s")
    
    return response
```

---

## ♻️ Other Common Middleware Uses

- **Adding Custom Headers**: Modifying the response to add custom headers (like security headers).
- **CORS (Cross-Origin Resource Sharing)**: Allowing or blocking requests from different domains.
- **Request Validation / Rates Limiting**: Checking rate limits before passing request down.

---

## 📁 Files in This Folder

```
9_middleware/
├── README.md   ← You are here
└── main.py     ← Simple logging middleware implementation
```

---

## ▶️ How to Run

```bash
cd 9_middleware
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

Look at your terminal console after sending requests in `/docs` to see the logged execution times.

---

## 🎯 Interview Questions

**Q1. What is middleware in a web framework?**
> Middleware is a function or component that intercepts HTTP requests before they reach the route handler, and intercepts responses before they are sent back to the client.

**Q2. How do you define a middleware in FastAPI?**
> You define middleware using the `@app.middleware("http")` decorator on an `async def` function that accepts `request` and `call_next` arguments.

**Q3. What is `call_next` in FastAPI middleware?**
> `call_next` is a function that forwards the incoming request to the next step in the application (either another middleware or the final route handler) and returns the generated response.

**Q4. Why must middleware handlers be defined as `async def`?**
> Because `call_next` is an asynchronous function that must be awaited (`await call_next(request)`), requiring the parent middleware function to be async.

**Q5. Can a middleware modify the response before sending it back?**
> Yes. After awaiting `call_next(request)` to get the response, you can modify its headers, body, or status code before returning it.

**Q6. What is the execution order when you have multiple middlewares?**
> Incoming requests pass through middlewares in the order they were added (top to bottom). Outgoing responses pass through them in reverse order (bottom to top).

**Q7. Can you block a request inside a middleware?**
> Yes. Instead of calling `await call_next(request)`, you can return a custom `JSONResponse` (e.g. `401 Unauthorized`) directly from the middleware, halting the request immediately.

**Q8. What is a common real-world use case for middleware?**
> Common use cases include logging requests (measuring processing time), handling CORS headers, adding security headers, tracking analytics, and global user-session processing.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
