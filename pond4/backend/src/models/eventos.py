from sqlalchemy import Column, Integer, String, Double, DateTime
from sqlalchemy.ext.declarative import declarative_base
from .base import Base

class Evento(Base):
    __tablename__ = 'eventos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    data_realizacao = Column(DateTime)
    data_criacao = Column(DateTime)
    data_modificacao = Column(DateTime)

    def __repr__(self):
        return f"<Evento(nome='{self.nome}', data de realização='{self.data_realizacao}', criado_em='{self.data_criacao}', modificado_em='{self.data_modificacao}')>"