# datetime: sets token expiry timestamps
# timedelta: sets token lifetime duration
from datetime import datetime, timedelta, timezone

# Depends: dependency injection tool
# HTTPException: returns HTTP error responses
# status: holds HTTP status constants
from fastapi import FastAPI, Depends, HTTPException, status

# OAuth2PasswordBearer: finds bearer token in Authorization header
# OAuth2PasswordRequestForm: parses login credentials from form-data
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# CryptContext: hashes and verifies passwords using Bcrypt
from passlib.context import CryptContext

# jwt: library to encode and decode signed JWT tokens
import jwt

app = FastAPI()

# SECRET_KEY: private string on server used to sign JWT signatures
SECRET_KEY = "my_super_secret_key_change_in_production"

# ALGORITHM: hashing algorithm used to sign JWT tokens
ALGORITHM = "HS256"

# ACCESS_TOKEN_EXPIRE_MINUTES: lifetime of the access token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context: password hasher machine configured with Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme: tells route handlers where to find/read token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# hash_password: turns plain text password into safe hash
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# verify_password: compares plain text login password with stored hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


fake_users_db = {
    "taha": {
        "username": "taha",
        "email": "taha@example.com",
        "hashed_password": hash_password("secret123"),
    }
}


# create_access_token: signs and generates a new access token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# get_current_user: verifies token signature and retrieves user object
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return {"username": user["username"], "email": user["email"]}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
