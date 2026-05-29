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

@app.put("/users/{user_id}")
async def updateuser(
    #here we pass the params that we want to update
    user_id : int,
    name : Optional[str] = None,
    email : Optional[str] = None,
    contact : Optional[str] = None,
    address : Optional[str] = None
):
    
    for person in users_db:
        if(person["id"] == user_id):

            if name is not None:
                person["name"] = name
            
            if email is not None:
                person["email"] = email
            
            if contact is not None:
                person["contact"] = contact

            if address is not None:
                person["address"] = address

    return{
        "message" : "User Updated Successfully",
    }

raise HTTPException(status_code = 404,detail = "User not found")
        

@app.patch("/users/{user_id}")
async def update_user(
    #here we pass the params that we want to update
    user_id : int,
    name : Optional[str] = None,
    email : Optional[str] = None,
    contact : Optional[str] = None
):
    
    for person in users_db:
        if(person["id"] == user_id):

            if name is not None:
                person["name"] = name
            
            if email is not None:
                person["email"] = email
            
            if contact is not None:
                person["contact"] = contact

    return{
        "message" : "User Updated Successfully",
    }

raise HTTPException(status_code = 404,detail = "User not found")
        

#other implementation of PUT.
@app.put("/user/{user_id}")
async def full_update_user(user_id: int, user: User):
    for person in users_db:
        if person["ID"] == user_id:
            person.update(user.dict())
            return {
                "message": "User Updated Successfully (PUT)",
                "updated_user": person
            }
    
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for index, person in enumerate(users_db):
        if person["id"] == user_id:
            users_db.pop(index)
            return {
                "status": "success",
                "message": f"User {user_id} deleted",
                "deleted_user_id": user_id
            }
    
    raise HTTPException(status_code=404, detail="User not found")

# so user_id is passed as path param to get user id, and then -  if(person["id"] == user_id): , 
# here it is used to check the fetched user id to verfiy


