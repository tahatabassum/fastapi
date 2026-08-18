import time
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    # Before request
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # After request
    process_time = time.time() - start_time
    print(f"Path: {request.url.path} | Time: {process_time:.6f}s")

    return response


@app.get("/")
def home():
    return {"message": "Welcome to the home page"}


@app.get("/slow")
def slow_route():
    time.sleep(0.5)  # Simulate a slow request
    return {"message": "This request was slow"}
