from fastapi import FastAPI, APIRouter, status, HTTPException, Depends, Path
from pydantic import BaseModel, Field
from database import sessionLocal
from auth import get_current_user
from sqlalchemy.orm import session
from typing import Annotated
from models import Users
from passlib.context import CryptContext

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

router = APIRouter(
    prefix="/user",
    tags=['user']
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict,Depends(get_current_user)]
db_dependency = Annotated[session,Depends(get_db)]

bcrypt_context = CryptContext(schemes=['argon2'],deprecated="auto")

@router.get("/", status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authenticatoion Faild")
    return db.query(Users).filter(Users.id == Users.get('id')).first()

# Change Password

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(user: user_dependency, db:db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Faild")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()