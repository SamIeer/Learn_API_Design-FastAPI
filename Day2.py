# API Architectural styles 
"""
1. REST : most populat api architecture for transferring data over the internet. 
In a restful context, resources are accessible via endpoints, and operations are performed on those resources
with standard  HTTP methods such as GET, POST, PUT and DELETE

2. Soap : stands for simple object access protocol, uses XML to transfer highly structured messages between a client and server.

3. GraphQL : Open source query language that enables clients to interact with a single API endpoint to retrieve the excat data they need,
without chaining multiple requests together

4. webhooks : webhooks are used to implement event-driven architectures, in ehich requests are automatically sent in response to event-based tiggers.

5. gRPC : RPC stands for remote procedure call, and grpc apis were originated by google

What are some common API use cases?
- Integrating with inernal and external systems
- Adding to enhancing functionality
- Connecting IoT devices
- Creating more scalable systems
- Reducing costs
- Improving organizational security and governace

"""
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional

# Initializing the app
app = FastAPI()

# Lets create a class for movies first 
class Movie:
    id: int
    title: str
    director: str
    genre: str
    rating: int

    def __init__(self, id, title, director, genre, rating):
        self.id = id
        self.title = title
        self.director = director
        self.genre = genre 
        self.rating = rating

class MovieRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=10)
    director: str = Field(min_length=15)
    genre: str = Field(min_length=1, max_length=10)
    rating: float = Field(gt=-1, lt=6)

MOVIES = [
    Movie(1, 'Inception', 'Christopher Nolan', 'Sci-Fi', 4.8),
    Movie(2, 'The Godfather', 'Francis Ford Coppola', 'Crime', 4.7),
    Movie(3, 'Spirited Away', 'Hayao Miyazaki', 'Animation', 4.8),
    Movie(4, 'Parasite', 'Bong Joon-ho', 'Thriller', 4.8),
    Movie(5, 'Pulp Fiction', 'Quentin Tarantino', 'Drama', 4.5),
]

# Get HTTP request for reading the data from server
@app.get("/movies")
def read_all_movies():
    return MOVIES

# Post HTTP request for creating data in the server
'''
It's a temporary for the server as we aren't using any database.
if we excute the same JSON again, the same movies added again again, if we add rating 333 it will work,
we don;t want both of these, we want some sort of validation so that id is unique and other properties of a movies set to a valid value
that's data validation
'''
'''
Pydantics and Data Validation
- Pydantics is a python library that is used for data mmodeling, data parsing and has efficient error handling
- It is commonly used for dara validation and how to handle data coming to out FastAPI application
Implementing pydantics in our project
- creating a different request model for dat validation
- adding a Field data validation on each variable/element
'''
# @app.post("/create-movie")
# # def create_movie(movie_request=Body()):
# #     MOVIES.append(movie_request)
# def create_movie(movie_request: MovieRequest):
#     new_movie = Movie(**movie_request.model_dump()) # The ** operator in the Movie() will pass the key-value from MovieRequest() to Movie() constructor (__int__())
#     # Movie(**movie_request.model_dump()) : We just converting the request to Movie object
#     MOVIES.append(new_movie)

