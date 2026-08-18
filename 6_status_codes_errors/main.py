from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


items = {
    1: {"name": "Laptop", "price": 999.99},
    2: {"name": "Phone", "price": 499.99},
}


class Item(BaseModel):
    name: str
    price: float


# 201 - item created
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    new_id = max(items.keys()) + 1
    items[new_id] = item.model_dump()
    return {"id": new_id, "item": item}


# 200 - get all items
@app.get("/items", status_code=status.HTTP_200_OK)
def get_items():
    return items


# 404 - item not found
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


# 204 - deleted, nothing returned
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items.pop(item_id)
