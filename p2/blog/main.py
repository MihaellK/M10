from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import sqlite3
import logging

#db
def create_database():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("'posts' table created!")

create_database()  # Call the function to create the database if it doesn't exist

# Database connection
def db_connect():
    return sqlite3.connect('posts.db')

# Log Config
logging.basicConfig(filename='prova2.log', level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Blog Post model
class BlogPost(BaseModel):
    id: int = None
    title: str
    content: str

app = FastAPI()

# CORS Setup
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.post("/blog", response_model=BlogPost, status_code=status.HTTP_201_CREATED)
async def post_blog(post: BlogPost):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (post.title, post.content))
    post.id = cursor.lastrowid  # Recupera o ID do último registro inserido
    con.commit()
    con.close()
    logger.warning(f"Post de id {post.id} Criado")
    return {**post.dict(), 'id': post.id}

@app.get("/blog")
async def get_blogs(response_model=list[BlogPost]):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = [BlogPost(id=row[0], title=row[1], content=row[2]) for row in cursor.fetchall()]
    con.close()
    logger.warning(f"Posts Recebidos")

    return posts

@app.get('/blog/{id}', response_model=BlogPost)
def get_blog_by_id(id: int):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (id,))
    post = cursor.fetchone()
    con.close()
    try:
        if post:
            logger.warning(f"Post de id {id} recebido")

            return BlogPost(id=post[0], title=post[1], content=post[2])
    except:
        logger.warning(f"post deu errado")
    
    raise HTTPException(status_code=404, detail='Blog Post not found :(')
    
    
# Update 
@app.put('/blog/{id}', response_model=BlogPost)
def update_blog_post(id: int, post: BlogPost):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (post.title, post.content, id))
    if cursor.rowcount == 0:
        con.close()
        raise HTTPException(status_code=404, detail='Blog Post not found')
    con.commit()
    con.close()
    logger.warning(f"Post de id {id} atualizado")

    return {**post.dict(), 'id': id}

# Delete route
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_post(id: int):
    con = db_connect()
    cursor = con.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (id,))
    if cursor.rowcount == 0:
        con.close()
        raise HTTPException(status_code=404, detail='Post not found')
    con.commit()
    con.close()
    logger.warning(f"Post de id {id} Deletado")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
