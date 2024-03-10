from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import create_session
from data_models import User
from utils import get_hashed_password

app = FastAPI()


@app.post("/signup/", summary="Create new user")
async def create_user(username: str, email: str, password: str, db: Session = Depends(create_session)):
    if db.query(User).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="User with this username already registered")

    elif db.query(User).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="User with this email already registered")

    password_hash = get_hashed_password(password)
    # Create new user
    new_user = User(username=username, email=email, password_hash=password_hash)

    # Add new User
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": "User registered successfully"}
