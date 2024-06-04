from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import sqlite3
import logging
#import db   #create db


# Database creation
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("'users' table created!")

create_database()  # Call the function to create the database if it doesn't exist

# Database connection
def db_connect():
    return sqlite3.connect('users.db')


class User(BaseModel):
    id: int = None
    username: str
    password: str


app = FastAPI()

# Configuração do logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


# CORS Setup
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.get('/users', response_model=list[User])
async def home():
    return 'get home'

@app.post("/register/")
async def register_user(user: User):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user.username, user.password))
        conn.commit()

        logger.info(f"User registered: {user.username}")
        return {"message": "User registered successfully"}
    except sqlite3.IntegrityError:
        logger.warning(f"Registration failed for user: {user.username} - Username already registered")

        raise HTTPException(status_code=400, detail="Username already registered")
    
    conn.close()

@app.post("/login/")
async def login_user(user: User):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM users WHERE username = ?', (user.username,))
    stored_password = cursor.fetchone()
    if stored_password is None or stored_password[0] != user.password:
        logger.warning(f"Login failed for user: {user.username} - Invalid username or password")

        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    logger.info(f"User logged in: {user.username}")
    return {"message": "Login successful"}
    
    conn.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)