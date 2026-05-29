# database.py - Super simple!
import sqlite3

# This function gives you a database connection
def get_db():
    conn = sqlite3.connect('myapp.db')  # Connect to file
    return conn

# Create tables when app starts
def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    ''')
    
    conn.commit()
    conn.close()