from fastapi import FastAPI
app=FastAPI()


#simple hello world return using get method
@app.get("/")
def hello():
    return {
        "message": "hello world"
    }




