# FastAPI Dependencies: A complete Guide 
# what are Dependencies
'''
Avoid code repetition
Share logic across multiple endpoints 
manage resources (like database connections)
Handle authentication and authorization
Validate requests
Think of dependencies as "helpers" that FastAPI automatically calls before running your endpoint.
'''
# With Dependencies 
# Define dependency once 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#use it everywhere
@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/posts/")
async def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all

# Common Use Cases
# -> Database Connection
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

## -> 2 Authentication
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify token and return user
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/profile/")
async def get_profile(currencent_user: User = Depends(get_current_user)):
    return {"username": currencent_user.username}

#->3 Type Alias (Cleaner code)
# instead of writing this wverywhere:
async def endpoint(db: Session = Depends(get_db)):
    pass

# Create a type alias:
db_dependency = Annotated[Session, Depends(get_db)]

#  Now use it:
async def endpoint(db: db_dependency):
    pass
