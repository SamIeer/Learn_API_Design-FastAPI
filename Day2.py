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
from fastapi import Body, FastAPI, Path
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
    released_year: int

    def __init__(self, id, title, director, genre, rating, released_year):
        self.id = id
        self.title = title
        self.director = director
        self.genre = genre 
        self.rating = rating
        self.released_year = released_year

class MovieRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=10)
    director: str = Field(min_length=15)
    genre: str = Field(min_length=1, max_length=10)
    rating: float = Field(gt=-1, lt=6)
    released_year: int = Field(gt=1980, lt=2026)

model_config = {
    "json_schema_extra":{
        "example": {
            "title": "A new movie",
            "director": "A movie director",
            "genre": "Comdey",
            "rating": 5,
            "released_date": 2020,
        }
    }
}
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

# More Pydantics Validation
'''
haven't added a validation to the movie's id 
Id should be unique and we shouldn't be able to give id for a movie.
Therfore, in order to add an id automatically that is greater than the last id by 1
'''
def find_movie_id(movie: Movie):
    if (len(MOVIES) > 0): #If we have a movie in our MOVIE list
        movie.id = MOVIES[-1].id + 1# add 1 to the last movie id 
    else:
        movie.id = 1 # if not set id to 1
    return movie

'''
The find_movie_id() function will create id for us so whatever id you have in the request body, 
it will overwrite it by giving the id greater than the last movie id by 1
To make this functionality work, we need to use this function inside our post request
'''
@app.post("/create-movie")
def create_movie(movie_request: MovieRequest):
    new_movie = Movie(**movie_request.model_dump())
    MOVIES.append(find_movie_id(new_movie))

# FETCH MOVIE
'''
Fetching movies by ID -> return the movie with the specific id you provide

'''
@app.get("/movies/{movie_id}")
def read_movie(movie_id: int = Path(gt=0)): # now if we searh a movie with id less than 0, get a 422 error
    for movie in MOVIES:
        if movie.id == movie_id:
            return movie
        
'''
Fetching movie by rating ->  This will fetch movies by their rating
We used a movies_to_return list here becuse there might be more than 1 movies with the same rating.
'''
@app.get("/movies/")
def read_movie_by_rating(movie_rating: float):
    movie_to_return = []
    for movie in MOVIES:
        if movie.rating == movie_rating:
            movie_to_return.append(movie)
    return movie_to_return


# Updating a Movie 
'''
One thing you will notice using this end point is, when you add a movie in the request body to update,
if you type in the id=1000 and try to update the movie, you will get status code 200 even though it didn't do anything.
'''
@app.put("/movies/update-movies")
def update_movies(movies: MovieRequest):
    for i in range(len(MOVIES)):
        if MOVIES[i].id == movies.id:
            MOVIES[i] = movies

@app.get("/movies/released_year/")
def read_movies_by_released_year(released_date: int):
    movie_to_return = []
    for movie in MOVIES:
        if movie.released_year == released_date:
            movie_to_return.append(movie)
    return movie_to_return

# Delet∈ a Movie
'''
Let's create an endpoint that deletes a movie
'''
@app.delete("/movies/{movie_id}")
def delete_movies(movie_id: int):
    for i in range(len(MOVIES)):
        if MOVIES[i].id == movie_id:
            MOVIES.pop(i)
            break


