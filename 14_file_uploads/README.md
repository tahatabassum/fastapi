# 📌 Module 14 — File Uploads & Static Files

This module covers how to handle incoming file uploads (images, PDFs, text files) and how to serve static assets (HTML, CSS, JS, images) from a local folder.

---

## 🧠 File Uploads: `File` vs `UploadFile`

FastAPI provides two ways to accept files in request bodies:

| Feature | `File` (as `bytes`) | `UploadFile` (recommended) |
|---|---|---|
| **Storage** | Entire file loaded into RAM. | Spooled in memory, written to disk if too large (doesn't exhaust RAM). |
| **Methods** | Raw byte operations. | Supports standard file-like methods (`read()`, `write()`, `seek()`, `close()`). |
| **Metadata** | None. | Provides file metadata like `filename`, `content_type`, and headers. |
| **Use Case** | Tiny files only. | Large files, images, PDFs, dynamic uploads. |

---

## 📁 Serving Static Files

Static files (stylesheets, javascript, static images) are served using the `StaticFiles` class from `fastapi.staticfiles`.
You "mount" a physical directory on a URL path:

```python
from fastapi.staticfiles import StaticFiles

# Mount the static directory on /static path
app.mount("/static", StaticFiles(directory="static"), name="static")
```

Now, a file at `static/image.png` will be accessible at `http://127.0.0.1:8000/static/image.png`.

---

## 📁 Folder Structure

```
14_file_uploads/
├── README.md       ← You are here
├── main.py         ← Main API file
└── static/         ← Directory for static files (created automatically)
```

---

## ▶️ How to Run

Install dependency:
```bash
pip install python-multipart
```
> ⚠️ **Note:** `python-multipart` is required by FastAPI to parse files sent as multi-part form data.

Run the server:
```bash
cd 14_file_uploads
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

---

## 🎯 Interview Questions

**Q1. What is the difference between using `bytes` and `UploadFile` for file uploads in FastAPI?**
> Using `bytes` loads the entire file into RAM, which can easily crash your server if a large file is uploaded. `UploadFile` uses a spooled file in memory (or writes it temporarily to disk if it exceeds a size limit), conserving memory. It also exposes metadata like `filename` and `content_type`.

**Q2. Why do you need `python-multipart` installed for file uploads to work in FastAPI?**
> HTTP file uploads are sent using the `multipart/form-data` encoding format. FastAPI requires the `python-multipart` package to parse this format. Without it, file uploads will raise a runtime error.

**Q3. How do you serve static files like images, CSS, or JS in FastAPI?**
> You mount an instance of `StaticFiles` to a specific path using `app.mount()`. For example: `app.mount("/static", StaticFiles(directory="static"), name="static")`.

**Q4. What is the significance of the `app.mount()` method?**
> `app.mount()` allows you to attach a completely independent sub-application (like `StaticFiles` or another FastAPI instance) to a specific path prefix, keeping it isolated from your main routing logic.

**Q5. How do you save an uploaded `UploadFile` to your local hard drive?**
> You open a local file in write-binary mode (`wb`), read the bytes from the uploaded file using `await file.read()`, and write them to the destination file. Always close the uploaded file using `await file.close()`.

**Q6. What file-like async methods does `UploadFile` support?**
> It supports `await file.read()`, `await file.write(data)`, `await file.seek(offset)`, and `await file.close()`.

**Q7. Can you validate file sizes or file types during upload in FastAPI?**
> Yes. You can inspect `file.content_type` (e.g., check if it starts with `image/`) or check the file size of the read bytes and raise an `HTTPException(status_code=400)` if they don't meet your criteria.

**Q8. What happens if you try to return the raw `UploadFile` object directly from a route?**
> FastAPI will fail to serialize it to JSON and return an error. You should instead return metadata (like the filename) or use a `FileResponse` if you want to stream the file back to the client.

---

*Part of the [FastAPI Learning Repository](https://github.com/tahatabassum/fastapi)*
