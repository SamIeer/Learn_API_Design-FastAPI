# Learning about whats API is and how its work
'''
An API, which stands for application programming interface, is a set of protocols that enable different
software components to cummunicate and transfer data.
Developers use APIs to bridge the gaps between samall, discrete chunks of code 
to create applications that are poweful, resilient, secure, abd able to meet uset needs.
HISTORY OF APIs
Commercial APIs 
Social media APIs
Cloud APIs
APIs for mobile apps
APIs for connected devices

HOW DO APUIs WORK : APIs work by sharing data between applications, systems ,and devices. This happens through request and response cycle.
The request is sent to the API, which retrieves the data and returns it to the user

1. API client : The client responsible for starting the convo by sending requests in different modes to API server
2. API request :  A request include the following components: Endpoint, Method, Parameters, Request headers, Request body
3. API Server : Responsible for handling authenication, validating input data, and retrieving or manipulating data.
4. API response : server response to the client : includes Status code, response headers, response body

What are the benefits of APIs
APIs connect various software systems, applications, and devices by allowing them to communicate with one another.
-Automation  -Innovation  -Security  -Cost efficieny

Different Types of APIs
- Private APIs  -Public APIs  -Partner APIs

FastAPI has something call SwaggerUI that will allow us to see all of our API enpoints
'''
# HTTP Reuest Methods
# HTTP request methodṡhave their own verbs attached to the CRUD operation that we need to use within our application
'''
Create -> POST
Read -> GET
Update -> PUT
Delete -> DELETE
'''

MOVIES = [
    {"title": "Inception", "director": "Christopher Nolan", "genre": "Sci-Fi"},
    {"title": "The Godfather", "director": "Francis Ford Coppola", "genre": "Crime"},
    {"title": "Spirited Away", "director": "Hayao Miyazaki", "genre": "Animation"},
    {"title": "Parasite", "director": "Bong Joon-ho", "genre": "Thriller"},
    {"title": "Pulp Fiction", "director": "Quentin Tarantino", "genre": "Drama"},
]

'''
GET HTTP Request Method
The GET request method is used to read data from the server without making any changes to it

uvicorn movies:app --reload  --> --reload the server restarts automatically when we save changes, so we just refresh the browser without rerunning the app
'''
from fastapi import FastAPI

app = FastAPI()

@app.get("/movies")  # endpoint calle /movies which return the list of movies of every movie we currently have
def read_all_movies():
    return MOVIES

