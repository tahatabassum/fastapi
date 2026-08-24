import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI()

STATIC_DIR = "static"

# Ensure the static directory exists
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Mount the static directory to serve files at http://127.0.0.1:8000/static/
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# 1. Upload using Bytes (loads everything into memory)
@app.post("/upload-bytes")
def upload_bytes(file: bytes = File(...)):
    return {"file_size": len(file)}


# 2. Upload using UploadFile (recommended for large files)
@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    # Simple validation: allow only images
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    # Define the save path
    file_path = os.path.join(STATIC_DIR, file.filename)

    # Save the file locally
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not save file")
    finally:
        await file.close()

    # Return metadata and URL to access it
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "url": f"/static/{file.filename}",
    }
