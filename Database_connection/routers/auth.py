from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel

from typing import Annotated
from sqlalchemy.orm import session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from database import sessionLocal
from models import Users

from passlib.context import CryptContext

SECRET_KEY = '1c13d4dc939b74a4f82b3e9b80c6aee6067f088ae924278a548cd806b1c24e80'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYW1zb24iLCJpZCI6MSwiZXhwIjoxNzcxNDI2NDU0fQ.DNY2akAbBhv743kLBrgMtKBhFKqtKwMEkEgOeg8GNLM")
'''
Why Use APIRouter
Keeps your project organinsed by seperating logic into differnt files.
Allows you to scale your application as it rows (eg, wuth, user.py, todos.py)
All routers can be included into the main app, so you still have one unified FastAPI application
'''
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)  # create a router using APIRouter -> This a;;ows us to include these routes inside our main application

bcrypt_context = CryptContext(schemes=['argon2'], deprecated="auto")
'''


'''


# We'll define a Pydantic model to valudare the incoming request
# Pydantic midel : va;idates the request body. it requires username, email, first_name, last_name, password and role
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

# Token Model   --> This pydantic mode defines the structure of the JWT response
class Token(BaseModel):
    access_token: str
    token_type: str

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
    return user

db_dependency = Annotated[session, Depends(get_db)]

@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed Authentication"   # If authentication fails -> return "Failed Authentication"
    token = create_access_token(user.username, user.id, timedelta(minutes=20)) # if authentication succeeds -> generate a JWT with username and user_id
    return {"access_token": token, "token_type": "Bearer"} # Return the JWT as access_token with tiken_type "Bearer"
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
    db.commit( )




'''
sub: standard JWT claim (subject -> here we store username).
id: user's unique ID
exp: expiration time -> ensures token will become invalid after the set duration
jwt.encode(..): creates the signed JWT string.
'''
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode tje Token 
'''
we create a dependency function get_current_user that will
Asscept the token from the request header
Decode it with the secret key and algorithm
Extract tje sub and id
if token is invalid or missing inforamation, raise a 401 unauthoriszed error
'''
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user"
            )
        return {"username": username, "id": user_id}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )
    
@router.post("/token", response_model=Token)
def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency)