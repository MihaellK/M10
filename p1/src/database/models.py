from sqlalchemy import Column, Integer, String, Boolean
from database.database import db

class Pedido(db.Model):
    __tablename__ = 'pedido'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    desc = Column(String(100), nullable=False)

    def __repr__(self):
        return f'<Pedido:[id:{self.id}, name:{self.name}, email:{self.email}, desc:{self.desc}]>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'desc': self.desc
        }

