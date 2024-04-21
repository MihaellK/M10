from sqlalchemy import Column, Integer, String, Boolean
from database.database import db

class User(db.Model):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False)
  password = Column(String(50), nullable=False)

  def __repr__(self):
    return f'<User:[id:{self.id}, name:{self.name}, email:{self.email}, password:{self.password}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "email": self.email,
      "password": self.password}
  
class Todo(db.Model):
  __tablename__ = 'todos'

  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(100), nullable=False)
  status = Column(Boolean, unique=False, default=False) 

  def __repr__(self):
    return f'<Todo:[id:{self.id}, title:{self.tilte}, status:{self.status}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "title": self.title,
      "status": self.status,
    }