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