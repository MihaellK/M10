from fastapi import HTTPException
from sqlalchemy.orm import Session
from repository.eventos import EventoRepository
from models.eventos import Evento
from schemas.eventos import Evento as EventoSchema

class EventoService:
    def __init__(self, db: Session):
        self.repository = EventoRepository(db)

    def get(self, evento_id):
        evento = self.repository.get(evento_id)
        if evento is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        return evento

    def get_all(self):
        return self.repository.get_all()

    def add(self, evento : EventoSchema):
        evento = Evento(**evento.dict())
        return self.repository.add(evento)

    def update(self, evento_id, evento : EventoSchema):
        evento = Evento(**evento.dict())
        return self.repository.update(evento_id, evento)

    def delete(self, evento_id):
        return self.repository.delete(evento_id)