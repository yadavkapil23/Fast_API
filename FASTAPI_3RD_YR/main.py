from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: str
    contact: int
    address: str

app = FastAPI()

users_db = []

@app.get("/home")
def get_home():
    return "This is the New User"

@app.get("/users/{user_id}")
def get_user(user_id : int):
    return {"ID of user is : ":user_id}

@app.get("/users")
async def get_filter(age:int=19, salary:int=50000):
    return {
        "Age is : " : age,
        "Salary is : " : salary
    }

@app.get("/products")
async def get_products(
    category : Optional[str] = None,
    min_price  : float = 0,
    max_price : Optional[float] = None,
    in_stock : bool = True
):
 return {
    "The Category is : " : category,
    "Minimum Price is : " : min_price,
    "IS PRODUCT IN STOCK : " : in_stock,
    "Maximum Retail Price : ": max_price
}

@app.post("/users")
async def create_users(
    id : int,
   name : str,
   email : str,
   contact : int,
   address : str
):

    user = {
        "ID" : id,
        "name": name,
        "email": email,
        "contact": contact,
        "address": address
    }

    users_db.append(user)
    return {
      "Message : " : "User Created Successfully",
      "User" : {
          "Id is : " : id,
         "Name of user : " : name,
         "Email of user : " : email,
         "phone number : " : contact,
         "nivaas sthaan : " : address
      }
   }

#getting a specific user.
@app.get("/getuser/{user_id}")
async def getspecfic_user(user_id : int):
    for person in users_db:
        if person["id"] == user_id:
            return person
        
        raise HTTPException(status_code = 404, info = "User not found")
    
#get more spefic details
@app.get("/search")
async def searching(
    id : int = None,
    name  : str =None,
    age : int = None
):
    result = []

    for person in users_db:

        if(
            (id is None or person["id"] == id) and #if id is not provided , then it ignores the id filtering and same for the name and age.
            (name is None or person["name"] == name) and
            (age is None or person["age"] == age)
        ):
            result.append(person)

    return{
        "total count" : len(result),
        "users" : result
    }