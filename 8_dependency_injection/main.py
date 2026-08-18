from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()


# Basic dependency
def get_db():
    return {"db": "connected"}


@app.get("/db-status")
def db_status(db=Depends(get_db)):
    return db


# Reusable pagination dependency #pagination means how much items to skip and how much items to return
def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/users")
def get_users(params=Depends(pagination)):
    return {"users": "list", "pagination": params}


@app.get("/items")
def get_items(params=Depends(pagination)):
    return {"items": "list", "pagination": params}


# Auth dependency
def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return x_token


@app.get("/secure-data")
def secure_route(token=Depends(verify_token)):
    return {"message": "Access granted", "token": token}


# Multiple dependencies
@app.get("/dashboard")
def dashboard(params=Depends(pagination), token=Depends(verify_token)):
    return {"pagination": params, "token": token}
