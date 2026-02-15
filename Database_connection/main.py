from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path, status
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
# GET TOdo by ID
'''
The endpoint path is /todo/{todo_id}
{todo_id} is a path parameter -> when the client makes a request like /todo/3, the value 3 is passed to the function
todo_id: int = Path(gt =0):
Ensure todo_id must be an integer, gt=0 means it must be greater than zero, if a user tries /todo/0 or /todo/-5, FastAPI automatically raises a validation error
'''
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK) # Status codes -> if request succeeds, it returns HTTP 200 OK, if the todo doesn't exist, we raise a 404 Not Found error.
def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    '''
    Querying the database
    Queries the Todos table for a reocrd where id == todo_id.
    .first() return the first matching record (or None if not found)
    Since id is a primary key, there can only be one match
    '''
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    '''
    If a todo is found, return it.
    if not, raise an HTTPException with:
    status_code=404 -> Not Found
    detail = "Todo not found" -> error message returned to the client
    '''
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

# Creating a New To-Do
from pydantic import BaseModel, Field

# Request model for creating a new todo 
'''
The TodoRequest Model : we created a Pydantic model called TodoRequest. This model defines the structure and validation rules for the data 
we expect when creating a new todo.  Note: we don't include id here because the database automatically generates it as the primary key
'''
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, it=6)
    complete: bool

'''
Defines a POST endpoint at /todo.
status_code=status.HTTP_201_CREATED -> tells swagger UI(and client) that this endpoint creates a new respurces
'''
@app.post("/todo", status_code=status.HTTP_201_CREATED)

# db: db_dependency -> injects a database session using our dependency injection.
#todo_request: TodoRequest -> FastAPI automatically validates the following JSON request against out Pydantic model 
def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

# db.add(todo_model) -> Prepares the new todo to be inserted into the database
# db.commit() -> finalizes the transaction and saves the todo.
    db.add(todo_model)
    db.commit()

'''
Updating the To-Do
create a PUT ENdpoint that updated an existing todo in the database
'''
@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    '''
    Updates each field of the existing todo with the new values from the request.
    The todo_request comes from our TodoRequest Pydantic model, which validates the input before it even reaches this function.
    '''
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()