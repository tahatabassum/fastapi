# 📌 Module 12 — Asynchronous Programming (Async/Await)

---

## 🧠 What is Async/Await?

**Asynchronous programming** is a technique that allows your web server to handle multiple requests concurrently without blocking execution. 

Instead of waiting for slow tasks (like database queries or external API calls) to finish before moving on, the server pauses the current task, works on other incoming requests, and resumes the paused task when its results are ready.

FastAPI is built on top of **Starlette** and is designed from the ground up to support asynchronous code natively.

---

## ⚙️ Concurrency vs Parallelism

* **Concurrency (Async):** One worker switches back and forth between multiple tasks. Perfect for **I/O-bound** tasks (waiting for database, reading files, fetching URLs).
* **Parallelism (Multi-core):** Multiple workers executing tasks at the exact same time. Perfect for **CPU-bound** tasks (heavy math, image processing).

FastAPI excels at **concurrency**!

---

## 🟢 `async def` vs `def` in FastAPI

FastAPI lets you define routes using either `async def` or regular `def`:

### 1. Using `async def` (Asynchronous)
Use this when you are doing **I/O-bound** operations and using library functions that support `async/await` (like async database drivers, `httpx`, or `asyncio`):

```python
import asyncio

@app.get("/async-data")
async def get_async_data():
    await asyncio.sleep(2) # Non-blocking sleep
    return {"message": "Done"}
```

### 2. Using `def` (Synchronous)
If you define a route with plain `def`, FastAPI runs it in an external **thread pool** automatically so it doesn't block the main event loop:

```python
import time

@app.get("/sync-data")
def get_sync_data():
    time.sleep(2) # Blocking sleep (run in thread pool)
    return {"message": "Done"}
```

> ⚠️ **Rule of Thumb:** If you are using a database library or external driver that *does not* support async (like standard SQLAlchemy or `requests`), define your routes using regular `def`. If your libraries support async, use `async def` and `await`.

---

## 📁 Folder Structure

```
12_async_await/
├── README.md   ← You are here
└── main.py     ← Async & Sync comparison examples
```

---

## ▶️ How to Run

```bash
cd 12_async_await
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

## 🎯 Interview Questions

**Q1. What is the difference between synchronous and asynchronous programming?**
> Synchronous code runs sequentially, meaning each line must finish executing before the next line begins, blocking the thread during slow operations. Asynchronous code allows a single thread to pause a slow task (like a DB query) and execute other tasks in the meantime, improving performance for I/O-bound applications.

**Q2. What is the Event Loop?**
> The Event Loop is the engine behind async programming. It continuously runs, tracks active asynchronous tasks, pauses them when they wait for I/O operations (like database or network calls), and resumes them as soon as those operations finish.

**Q3. When should you use `async def` vs regular `def` in FastAPI?**
> Use `async def` if you are performing I/O-bound tasks and using libraries that support `async/await` (e.g., `httpx` or an async database driver). Use regular `def` if you are using synchronous libraries (like standard `requests` or standard SQLite/SQLAlchemy) because FastAPI runs regular `def` functions in a separate thread pool to prevent blocking the main loop.

**Q4. What happens if you run a blocking synchronous operation (like `time.sleep()`) inside an `async def` function?**
> It blocks the entire event loop. Because the event loop runs on a single thread, any blocking call inside `async def` freezes the entire server, meaning no other concurrent requests can be processed until the block finishes.

**Q5. What is the purpose of the `await` keyword?**
> The `await` keyword passes execution control back to the event loop. It tells the loop: "This step will take some time, pause this function here and run other tasks until this returns a result." You can only use `await` inside an `async def` function.

**Q6. What is the difference between Concurrency and Parallelism?**
> Concurrency is about *dealing* with multiple tasks at once by rapidly switching between them (like one cook working on three dishes). Parallelism is about *executing* multiple tasks at the exact same time using multiple CPU cores (like three cooks working on three separate dishes).

**Q7. Is FastAPI faster than Flask because of async?**
> Yes, for I/O-bound tasks. Flask is synchronous by default, meaning each request blocks a thread. FastAPI uses ASGI and an event loop, allowing a single process to handle thousands of concurrent requests without blocking, resulting in much higher throughput.

**Q8. What Python module is commonly used to write asynchronous sleep, gather tasks, and manage loops?**
> The built-in `asyncio` module is used for writing asynchronous concurrent code in Python.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
