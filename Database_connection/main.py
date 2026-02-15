from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models
from models import Todos
from database import sessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
'''
Creates all the databse tables defined in our models.py
if the todos table does not exist, this line will generate it inside our Todolist,db file
'''

def get_db():
    db = sessionLocal()  # create a new database session
    try:
        yield db   # gives this session to whatever function needs it (out API endpoint)
    finally:       # Once the request is done, the session iṡclosed to free resources
        db.close()
# This pattern makes sure the database connection is opended and closed safely for every request

'''
This defines a dependency we can reuse 
Dependecy = a function that provides something our route needs( in this case, a DB session)
Instead of creating a session in every endpoint, we just say " this route depends on get_db"
Using Annotated makes type hints clearer: FastAPI knows it should inject a Session into our function
'''
db_dependency = Annotated[Session, Depends(get_db)]  


@app.get("/")  # Defines a GET endpoint at the root path /, When a client requests /, FastAPI calls read_all
def read_all(db: db_dependency): # db: db_dependency -> tells FastAPI: " inject a database session here using get_db", Inside the function, we can use db to run queries
    return db.query(Todos).all()  # Runs a query on the Todos table .all() -> returns all rows as a list, 
    # FastAPI automatically serializes these toes into JSON and sends them back to the client
'''
WHY USe Dependencies?
Without dependencies, we sould have to mabually create and close the database session in every single endpoint.
With dependencies, we write once and reuse everywhere.
makes code : Cleaner , Easier to test, Less error - prone
'''