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

'''
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}