import asyncio
import time
from fastapi import FastAPI

app = FastAPI()


# Synchronous Route (run in a thread pool by FastAPI)
@app.get("/sync-sleep")
def sync_sleep():
    time.sleep(2)  # Blocking sleep
    return {"message": "Sync sleep finished"}


# Asynchronous Route (run directly on the event loop)
@app.get("/async-sleep")
async def async_sleep():
    await asyncio.sleep(2)  # Non-blocking sleep
    return {"message": "Async sleep finished"}
