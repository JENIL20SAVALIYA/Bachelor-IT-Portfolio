from models.models import User as UserModel
from fastapi import FastAPI, APIRouter, Depends, HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from schema.Schema import User
from utils.hash_pass import hash_password, verify_password
from utils.jwt_handler import create_access_token
from sqlalchemy import or_
from fastapi.security import OAuth2PasswordRequestForm
from utils.send_mail import send_mail


router = APIRouter()

@router.post("/signUp")
def create_user(
    user: User,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db)
):
    existing_user = db.query(UserModel).filter(
        or_(UserModel.email == user.email, UserModel.username == user.username)
    ).first()

    if existing_user:
        return {"message": "This user already exists"}

    hashed_pass = hash_password(user.password)
    new_user = UserModel(username=user.username, email=user.email, password=hashed_pass)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Run email sending in background
    background_task.add_task(
        send_mail,
        user.email,
       message = f"""
        Hi {user.username},

    🎉 Welcome to Job Board — where your dream job is just a click away!

    We're excited to have you on board. Start exploring top opportunities tailored for you.

    🧾 Your login details:
    Username: {user.username}
    Password: {user.password}

    👉 Start applying and claim your dream job today!

        Best regards,  
        Job Board Team
        """

    )

    return {"message": "Your account was created successfully."}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(UserModel).filter(
        or_(
            UserModel.email == form_data.username,
            UserModel.username == form_data.username
        )
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect Password")

    token = create_access_token({"sub": user.email, "username": user.username})
    return {"access_token": token, "token_type": "bearer"}