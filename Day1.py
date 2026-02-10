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
from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/movies")  # endpoint calle /movies which return the list of movies of every movie we currently have
def read_all_movies():
    return MOVIES

# Path and Query Parameters
'''
Path Parameters: Path parameters are variables that are part of the URL path itself. They allow you to capture values directly from the URL
Example URL: https://jsonplaceholder.typicode.com/posts/5
From the URL we have: 
Base URL: https://jsonplaceholder.typicode.com
Path: /posts/{id}
Path parameter: id 
Path parameter value: 5
In FastAPI, path parameter id define using {}, which makes that part of the path dynamic
By dynamic, we mean that we can change the value in that part of the URL, and FastAPI will capture it and pass it to our function
'''
# @app.get("/movies/{title}") # title is a dynamic method
# def read_movie(title):
#     return {"Movie title": title}

# Order of Endpoint Declaration in FastAPI
# In FastAPI the order of route declarations matters when path parameters.
@app.get("/movies/{dynamic_param}")
def read_all_movies(dynamic_param: str):
    return {"movie title": dynamic_param}

# @app.get("/movies/mymovie")
# def read_favorite_movie():
#     return {"movie title": "My favorite movie"}

# The second route will never be reached because the dynamic one already captured the request

# When we type a request that needs a space we are gping to use %20 instead of the space
@app.get("/movies/{title}")
def read_movie(title: str): # type is declared here
    for movie in MOVIES:
        if movie.get('title').casefold == title.casefold():
            return movie
# casefold() is similar to lower() method, bit the casefold() method is stronger, more aggressive

# Path Parameters with Type Hints
# we can define the type of the path parameter in the function using Python type hints. FastAPI will
'''
Convert the parameter to the specified type
Validate the value before calling the function
We are setting the path parameter title to be a string type. The validation is handled by pydantic
'''

# Query Parameters
"""Query parameters are request parameters in the URL after a question mark(?). 
Multiple parameters are separated by an ampersand(&)  
In FastAPI, query parameters are simply function arguments that are not part of the path
"""      
@app.get("/movies/")   
def read_genre_by_query(genre: str):
    movies_to_return = []            
    for movie in MOVIES:
        if movie.get('genre').casefold() == genre.casefold():
            movies_to_return.append(movie)  
    return movies_to_return                          

