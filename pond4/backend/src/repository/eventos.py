from models.eventos import Evento
from sqlalchemy.orm import Session
from datetime import datetime

class EventoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, evento_id):
        return self.db.query(Evento).get(evento_id)

    def get_all(self):
        return self.db.query(Evento).all()

    def add(self, evento: Evento):
        evento.id = None
        evento.data_criacao = datetime.now()
        self.db.add(evento)
        self.db.flush()
        self.db.commit()
        return {"message": "Evento cadastrado com sucesso"}

    def update(self, evento_id, evento):
        eventodb = self.db.query(Evento).filter(Evento.id == evento_id).first()
        if eventodb is None:
            return {"message": "Evento não encontrado"}
        evento.data_modificacao = datetime.now()
        evento = evento.__dict__
        evento.pop("_sa_instance_state")
        evento.pop("data_criacao")
        evento.pop("id")
        self.db.query(Evento).filter(Evento.id == evento_id).update(evento)
        self.db.flush()
        self.db.commit()
        return {"message": "Evento atualizado com sucesso"}

    def delete(self, evento_id):
        eventodb = self.db.query(Evento).filter(Evento.id == evento_id).first()
        if eventodb is None:
            return {"message": "Evento não encontrado"}
        self.db.query(Evento).filter(Evento.id == evento_id).delete()
        self.db.flush()
        self.db.commit()
        return {"message": "Evento deletado com sucesso"}
        