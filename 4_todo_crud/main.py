from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


todos = {}
counter = 1


@app.post("/todos")
def create_todo(todo: Todo):
    global counter
    todos[counter] = todo
    counter += 1
    return {"id": counter - 1, "todo": todo}


@app.get("/todos")
def get_todos():
    return todos


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = todo
    return {"message": "Todo updated", "todo": todo}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(todo_id)
    return {"message": "Todo deleted"}
