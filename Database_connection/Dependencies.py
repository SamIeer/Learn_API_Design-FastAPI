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

'''
How FastAPI processes parameters
'''
# PAth Parameters
@app.get("/uisers/{user_id}")
async def get_user(user_id: int): # <- Path parameter
    pass

# Dependencies
@app.get("/users/")
async def get_users(db: Session = Depends(get_db)): # <- Dependency
    pass

# Query parameter
@app.get("/users/")
async def  get_users(skip: int = 0, limit: int = 10 ): # <- Query parameter
    pass

# Request body
@app.get("/users/")
async def create_user(user: Usrcreate): # <- Request body
    pass

"""
Order Rule : Why it matters
"""
# Wrong order 
@app.get("/callback")
async def auth_google(code: str = None, db: Session = Depends(get_db)):
    pass

# Correct order
@app.get("/callback")
async def auth_google(db: Session = Depends(get_db), code: str = None):
    pass

'''
why?
python requires non-default parameters to come before default parameters
'''
#py error
def func(a=1,b): # can't put a non-default 'b' after default 'a'
    pass
def func(b, a=1): # non-default first, then defaults
    pass

'''
Even though db: Session = Depends(get_db) looks like it has a default,
FastAPI treats dependencies as non-default parameters internally. 
So they must come before optional query parameters.
'''
# Complete Example
from typing import Annotated

app = FastAPI()

#1 Define dependency
def get_db()
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

#2 Create type alias
db_dependency = Annotated[Session, Depends(get_db)]

#3 Use in endpoints with correct order
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,  # path parameter
    db: db_dependency,  # Dependency 
    include_posts: bool = False # 3. Query parameter
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/")
async def create_user(
    db: db_dependency, # 1. Dependeccy (np path params here)
    user_data: UserCreate # 2. Request body
):
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    return new_user

'''
Key Takeaways
1. Dependencies = Resuable code that FastAPI automatically injects
2. Always put dependencies BEFORE optional parameters
3. Use typw aliases(db_dependency) for cleaner code
4. Dependencies run automatically before your endpoint function
5. Order matters: Path -> Dependencies -> Query -> Body
'''
# Common patterns 
# pattern 1: Chained Depends
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # This dependency uses another dependency (get_db)
    return verify_token(db, token)

@app.get("/profile/")
async def profile(user: User = Depends(get_current_user)):
    # get_current_user automatically calls get_db
    return user

# Pattern 2: Optional Dependencies
def get_optional_user(token: str = None):
    if token:
        return verify_token(token)
    return None

@app.get("/posts/")
async def get_posts(user: User = Depends(get_optional_user)):
    # user can be None if no token provided
    if user:
        return get_user_posts(user)
    return get_public_posts()