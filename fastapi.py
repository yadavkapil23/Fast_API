from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# ---------- DATABASE SETUP ----------
def get_db():
    """Create database connection"""
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def setup_database():
    """Create users table if not exists"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contact INTEGER NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

# Run setup when app starts
setup_database()

# ---------- PYDANTIC MODELS ----------
class User(BaseModel):
    name: str
    email: str
    contact: int
    address: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[int] = None
    address: Optional[str] = None

# ---------- HOME ----------
@app.get("/home")
def get_home():
    return "This is the New User"

# ---------- GET USER BY ID (PATH PARAMETER) ----------
@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return dict(user)

# ---------- GET FILTER (QUERY PARAMETERS) ----------
@app.get("/users")
async def get_filter(age: int = 19, salary: int = 50000):
    # This is just a demo endpoint - not using database
    return {
        "Age is: ": age,
        "Salary is: ": salary
    }

# ---------- GET PRODUCTS (QUERY PARAMETERS) ----------
@app.get("/products")
async def get_products(
    category: Optional[str] = None,
    min_price: float = 0,
    max_price: Optional[float] = None,
    in_stock: bool = True
):
    return {
        "The Category is: ": category,
        "Minimum Price is: ": min_price,
        "IS PRODUCT IN STOCK: ": in_stock,
        "Maximum Retail Price: ": max_price
    }

# ---------- CREATE USER (POST) ----------
@app.post("/users")
async def create_users(
    id: int,
    name: str,
    email: str,
    contact: int,
    address: str
):
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Note: We're using the provided id instead of AUTOINCREMENT
        cursor.execute('''
            INSERT INTO users (id, name, email, contact, address)
            VALUES (?, ?, ?, ?, ?)
        ''', (id, name, email, contact, address))
        
        conn.commit()
        
        return {
            "Message: ": "User Created Successfully",
            "User": {
                "Id is: ": id,
                "Name of user: ": name,
                "Email of user: ": email,
                "phone number: ": contact,
                "nivaas sthaan: ": address
            }
        }
    
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User ID or Email already exists")
    
    finally:
        conn.close()

# ---------- UPDATE USER (PUT - Partial Update like PATCH) ----------
@app.put("/users/{user_id}")
async def update_user(
    user_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    contact: Optional[int] = None,
    address: Optional[str] = None
):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()
    
    if existing_user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build dynamic update query
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = ?")
        values.append(name)
    
    if email is not None:
        updates.append("email = ?")
        values.append(email)
    
    if contact is not None:
        updates.append("contact = ?")
        values.append(contact)
    
    if address is not None:
        updates.append("address = ?")
        values.append(address)
    
    if updates:
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        values.append(user_id)
        cursor.execute(query, values)
        conn.commit()
    
    # Get updated user
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    updated_user = cursor.fetchone()
    conn.close()
    
    return {
        "message": "User Updated Successfully",
        "user": dict(updated_user)
    }

# ---------- PARTIAL UPDATE (PATCH) ----------
@app.patch("/users/{user_id}")
async def patch_user(
    user_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    contact: Optional[int] = None,
    address: Optional[str] = None
):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()
    
    if existing_user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build dynamic update query (same as PUT)
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = ?")
        values.append(name)
    
    if email is not None:
        updates.append("email = ?")
        values.append(email)
    
    if contact is not None:
        updates.append("contact = ?")
        values.append(contact)
    
    if address is not None:
        updates.append("address = ?")
        values.append(address)
    
    if updates:
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        values.append(user_id)
        cursor.execute(query, values)
        conn.commit()
    
    # Get updated user
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    updated_user = cursor.fetchone()
    conn.close()
    
    return {
        "message": "User Partially Updated Successfully (PATCH)",
        "user": dict(updated_user)
    }

# ---------- FULL REPLACEMENT (PUT with all fields) ----------
@app.put("/user/{user_id}")
async def full_update_user(user_id: int, user: User):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()
    
    if existing_user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Full replacement
    cursor.execute('''
        UPDATE users 
        SET name = ?, email = ?, contact = ?, address = ?
        WHERE id = ?
    ''', (user.name, user.email, user.contact, user.address, user_id))
    
    conn.commit()
    
    # Get updated user
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    updated_user = cursor.fetchone()
    conn.close()
    
    return {
        "message": "User Fully Replaced Successfully (PUT)",
        "updated_user": dict(updated_user)
    }

# ---------- DELETE USER ----------
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {
        "message": f"User {user_id} deleted successfully",
        "deleted_user": dict(user)
    }

# ---------- GET ALL USERS (Helper endpoint) ----------
@app.get("/all-users")
async def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return {"users": [dict(user) for user in users]}