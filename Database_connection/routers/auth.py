from fastapi import FastAPI, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from typing import Annotated
from sqlalchemy.orm import session

from database import sessionLocal
from models import Users

from passlib.context import CryptContext

'''
Why Use APIRouter
Keeps your project organinsed by seperating logic into differnt files.
Allows you to scale your application as it rows (eg, wuth, user.py, todos.py)
All routers can be included into the main app, so you still have one unified FastAPI application
'''
router = APIRouter()  # create a router using APIRouter -> This a;;ows us to include these routes inside our main application

bcrypt_context = CryptContext(schemes=['argon2'], deprecated="auto")
'''


'''

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

db_dependency = Annotated[session, Depends(get_db)]
# We'll define a Pydantic model to valudare the incoming request
# Pydantic midel : va;idates the request body. it requires username, email, first_name, last_name, password and role
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

'''
Recieves a validate createuserrequest
Builds a users ORM object by mapping fields from the rquest to the model
sets is_active=True by default
returns the created ORM object
'''
@router.post("/auth/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, create_user_request: CreateUserRequest):   # Define a simple endppoint ar /auth/ which returns a JSON response
    create_user_model = Users(
        # Build a Users ORM object from it
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit(  )

@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed Authentication"
    return "Successfully authenticated"