from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database creation
def create_database():
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("'todos' Table created!")

create_database()  # Call the function to create the database if it doesn't exist

# Database connection
def db_connect():
    return sqlite3.connect('todos.db')

# Pydantic model
class Todo(BaseModel):
    id: int = None
    title: str
    status: int

# CORS Setup
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Get all to-dos route
@app.get('/todos', response_model=list[Todo])
def get_todos():
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = [Todo(id=row[0], title=row[1], status=row[2]) for row in cursor.fetchall()]
    con.close()
    return todos

# Get one todo by id
@app.get('/todos/{id}', response_model=Todo)
def get_todo_by_id(id: int):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM todos WHERE id = ?', (id,))
    todo = cursor.fetchone()
    con.close()
    if todo:
        return Todo(id=todo[0], title=todo[1], status=todo[2])
    raise HTTPException(status_code=404, detail='To-do not found :(')

# POST todo route
@app.post('/todos', response_model=Todo, status_code=status.HTTP_201_CREATED)
def post_todo(todo: Todo):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('INSERT INTO todos (title, status) VALUES (?, ?)', (todo.title, todo.status))
    todo.id = cursor.lastrowid  # Recupera o ID do último registro inserido
    con.commit()
    con.close()
    return {**todo.dict(), 'id': todo.id}

# Update Todo route
@app.put('/todos/{id}', response_model=Todo)
def update_todo(id: int, todo: Todo):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('UPDATE todos SET title = ?, status = ? WHERE id = ?', (todo.title, todo.status, id))
    if cursor.rowcount == 0:
        con.close()
        raise HTTPException(status_code=404, detail='to-do not found')
    con.commit()
    con.close()
    return {**todo.dict(), 'id': id}

# Delete Todo route
@app.delete('/todos/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (id,))
    if cursor.rowcount == 0:
        con.close()
        raise HTTPException(status_code=404, detail='Note not found')
    con.commit()
    con.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# run app
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
