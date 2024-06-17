from pydantic import BaseModel
from datetime import datetime

class Evento(BaseModel):
    id: int
    nome: str
    data_realizacao: datetime
    data_criacao: datetime
    data_modificacao: datetime

    class Config:
        orm_mode = True