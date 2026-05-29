# routers/users.py - The actual API endpoints
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import UserCreate, UserUpdate, UserResponse
from services import UserService

# Create router
router = APIRouter()

# GET all users
@router.get("/users")
def get_all_users(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return {"users": users}

# GET one user
@router.get("/users/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(404, "User not found")
    
    return {"user": user}

# CREATE user
@router.post("/users")
def create_user(user: UserCreate, db=Depends(get_db)):
    # Use service for business logic
    result = UserService.create_user(db, user.name, user.email)
    return result

# UPDATE user
@router.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db=Depends(get_db)):
    cursor = db.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        raise HTTPException(404, "User not found")
    
    # Update only provided fields
    if user.name:
        cursor.execute("UPDATE users SET name = ? WHERE id = ?", 
                      (user.name, user_id))
    
    if user.email:
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", 
                      (user.email, user_id))
    
    db.commit()
    return {"message": "User updated"}

# DELETE user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    
    return {"message": "User deleted"}