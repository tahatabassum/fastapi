from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


items = {
    1: {"name": "Laptop", "price": 999.99},
    2: {"name": "Phone", "price": 499.99},
}


class Item(BaseModel):
    name: str
    price: float


# Custom exception
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id


# Global handler for custom exception
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Item {exc.item_id} does not exist"}
    )


# Using HTTPException (simple way)
@app.get("/items/{item_id}")
def get_item_http(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


# Using custom exception + global handler
@app.get("/items/custom/{item_id}")
def get_item_custom(item_id: int):
    if item_id not in items:
        raise ItemNotFoundError(item_id=item_id)
    return items[item_id]
