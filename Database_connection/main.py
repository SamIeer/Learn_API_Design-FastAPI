from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models
from models import Todos
from database import sessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def read_all(db: db_dependency):
    return db.query(Todos).all()