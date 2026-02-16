from fastapi import FastAPI, APIRouter

router = APIRouter()  # create a router using APIRouter -> This a;;ows us to include these routes inside our main application

@router.get("/auth/")
def get_user():   # Define a simple endppoint ar /auth/ which returns a JSON response
    return {"user": "authentication"}