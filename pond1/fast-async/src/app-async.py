# Backend assincrono com FastAPI

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import sqlite3

app = FastAPI()

#db connect
def db_connect():
    return sqlite3.connect('todos.db')

#pydantic model
class Todo(BaseModel):
    id: int
    title: str
    status: int

#CORS Setup
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Get all to-dos route
@app.get('/todos', response_model=List[Todo])
def get_todos():
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = [Todo(id=row[0], title=row[1], status=row[2]) for row in cursor.fetchall()]
    con.close()
    return todos

# Get one todo by id
@app.get('/todos/{id}', response_model=List[Todo])
def get_todo_by_id(id: int):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM todos WHERE id = ?', (id))
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
    cursor.execute('INSERT INTO todos (title, status) Values (?,?,?)', (todo.title, todo.status))
    con.commit()
    con.close()
    return {**tarefa.dict(, 'id': tarefa.id)}

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
def delete_todo(id: int)
    con = conectar_bd()
    cursor = con.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (id))
    if cursosr.rowcount == 0:
        con.close()
        raise HTTPException(status_code=404, detail='Note not found')
    con.commit()
    con.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# run app
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)