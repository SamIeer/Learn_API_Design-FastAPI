#Testing Overview
'''
What is Testing 
it is a way for us to make sure our application working as intended
part of software development lifecycle that aims to identify:
-> Bugs -> Error -> Deffects
Meets user requirements and specifications
Ensuring software is high quality, reliabe, secure and user friendly

Manual Testing 
it is the testing have been doing so far
We have been manuallhy running our application and testing our api endpoints and other functionalities if they are 
working or not. That is manual testing

Unit Testing
Involves testing individual components or units of software is isolation from the rest of the application
Validatess that each unit of the software performs as designed 
unit = Testable part of the application
Developers wright unit tests during the development phase
Tests are automated and execures by a testing framework (Pytest)
Benefir is to identify bugs early in the development process

Integration Testing
Focisess on testing the interactions between different units ot components units togehter
Helps identify problems for the entire solution
Example: Call an API endpoint and make sure the correct solution is returned

Pytest:
Popular testing framework for python
known for simplicity, scalablility and ability to handle both unit and integration tests
TOp reasons to use Pytest:s
Simple and Flexible - Native Assertions
Fixtures - Features setup and teardown
Parameterized testing - Run same tests with different data
'''

# Getting started with Testing
'''
First Step 
create a new directory on our project called test
inside out rest directory, create a new file called __init__.py
inside out test directoy, create abother file called test_example.py

test_example.py
Pytest will run all tests automatically that sit within files that have the name 'test' in them
For our demo, all tests will be in test_example.py so Pytest can find them easily
when we write tests for our application, we will create new tests from a new file that matches naminf convention of project 
Example: todos.py will be testd test_todos.py

Create our First unit test
Write our first assertion test
Asserion = statement that checks if a condition is true 
if contition is true = test passes
if condition is false = test fails 

# test_example.py
def test_equla_or_not():
assert 3 == 3

def test_equal_or_not_equal(): # fail
   assert 3 == 3  # pass
   assert 3 == 2  # fail
   assert 3 != 1  # pass 
   assert 3 != 3 # fail 
'''  
import pytest

def equal_or_not():
    assert 3 == 3 

# What a test function looks like
def test_something():
    assert something == expected

# 
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)
def test_ping():
    responmse = client.get("/ping")
    assert responmse.status_code == 20
    assert responmse.json() == {"message": "pong"}

'''
What you need to know beforoe writting tests 
Step1 - Start with testing endpoints (easisedt entry point)
step 2 - what should you test
-> status code 
-> Response body
asser response.json()["name"] == "john"
-> validation errors 
response = client.post("/users",json={})
assert response.status_code == 422

Step 3 - Waht you should learn next 
-> fixtures(very important)
@pytest.fixture -> makes the code clean and scalable
def client():
return testclient(app)

def test_ping(client):
response = client.get("/ping")
assert response.status_code == 200

-> Testing dependencies(database, auth)
Depends(get_db)

What order should you learn in 
phase 1
basic endpint tests 
status code assertions 
json response asserions
pytest basics

phase 2
fixtures
parametrized test
testing Post/Put with payload

phase3
'testing database (sqlite test db)
dependency overrides
mocking external services

phase 4 (advanced)
async testing 
coverage reports 
ci integration

'''
# probabalẏgp for async now 
''''
In python async is about non-blocking I/O not "making things magically faster"
it lets your app:
start a test 
pause it while waiting 
handle other requests during that wait 
resume when ready

How fastAPI is built on:
asyncio 
starlette
uvicorn(ASGI server)
ASGI supports async natively
'''
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def read_root():
    return {"message":"hello world"}

'''
That async means:
This route runs inside an event loop
it can await async opeartions
it won't block other requests while waiting
'''

'''
The Event Loop 
imagine a single worker that:
keeps a list of tasks
switches between them when one is waiting
This is the event loop

When should you use async def 
use async def when:
you're calling an async DB driver (like asyncpg)
you're calling an async HTTP client (like httpx async)
you're doing async file I/O
You're awaiting anything
'''
import httpx 
@app.get("/external")
async def call_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
    return response.json()
# Notice:
# async def 
# await inside it 
# that's proper async usage