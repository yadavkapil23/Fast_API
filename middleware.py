#CODE THAT RUNS BEFORE AND AFTER EVERY REQUEST

from fastapi import FastAPI, Request
import time

app = FastAPI()

# SIMPLE MIDDLEWARE
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # BEFORE request - runs first
    print(f"Request received: {request.method} {request.url}")
    
    # Process the request (call your API)
    response = await call_next(request)
    
    # AFTER request - runs last
    print(f"Response sent: {response.status_code}")
    
    return response

@app.get("/")
def home():
    return {"message": "Hello"}
