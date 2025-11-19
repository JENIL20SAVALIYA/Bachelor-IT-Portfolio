from fastapi import Header,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_handler import verify_token
from sqlalchemy.orm import Session
from database import get_db
from models.models import User as UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db) ):
    
    print("recived token",token)
    payload = verify_token(token)

    print("Decoded payload:", payload)


    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(UserModel).filter(UserModel.email == email).first()

    print("Extracted email:", email)
    print("User found:", user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user