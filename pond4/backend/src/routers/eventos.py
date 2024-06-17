from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.eventos import Evento as EventoSchema
from services.eventos import EventoService
from databases import database
import logging

logging.basicConfig(filename='logs/eventos_app.log', level=logging.INFO, format='{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}')

LOGGER = logging.getLogger(__name__)

router = APIRouter()

@router.get("/eventos/{evento_id}")
async def get_evento(evento_id: int, db: Session = Depends(database.get_db)):
    LOGGER.info({"message": "Acessando a rota /eventos/{evento_id}", "evento_id": evento_id, "method": "GET"})
    eventoService = EventoService(db)
    return eventoService.get(evento_id)

@router.get("/eventos")
async def get_eventos(db: Session = Depends(database.get_db)):
    LOGGER.info({"message": "Acessando a rota /eventos", "method": "GET"})
    eventoService = EventoService(db)
    return eventoService.get_all()

@router.post("/eventos")
async def create_evento(evento: EventoSchema, db: Session = Depends(database.get_db)):
    LOGGER.info({"message": "Acessando a rota /eventos", "method": "POST", "evento": evento.dict()})
    eventoService = EventoService(db)
    return eventoService.add(evento=evento)

@router.put("/eventos/{evento_id}")
async def update_evento(evento_id: int, evento: EventoSchema, db: Session = Depends(database.get_db)):
    LOGGER.info({"message": "Acessando a rota /eventos/{evento_id}", "method": "PUT", "evento_id": evento_id, "evento": evento.dict()})
    eventoService = EventoService(db)
    return eventoService.update(evento_id, evento=evento)
    

@router.delete("/eventos/{evento_id}")
async def delete_evento(evento_id: int, db: Session = Depends(database.get_db)):
    LOGGER.info({"message": "Acessando a rota /eventos/{evento_id}", "method": "DELETE", "evento_id": evento_id})
    eventoService = EventoService(db)
    return eventoService.delete(evento_id)