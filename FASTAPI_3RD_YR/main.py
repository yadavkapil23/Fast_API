from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
   id:int
   age:int
   salary:int
   category:str
   min_price:float
   max_price:float
   in_stock:bool

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
   name : str,
   email : str,
   contact : int,
   address : str
):

    user = {
        "name": name,
        "email": email,
        "contact": contact,
        "address": address
    }

    users_db.append(user)
    return {
      "Message : " : "User Created Successfully",
      "User" : {
         "Name of user : " : name,
         "Email of user : " : email,
         "phone number : " : contact,
         "nivaas sthaan : " : address
      }
   }