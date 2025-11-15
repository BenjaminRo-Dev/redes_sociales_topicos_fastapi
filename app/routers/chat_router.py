from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest
from app.services.chat_service import generar_contenido

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/generar", response_model=dict)
def obtener_contenido(solicitud: ChatRequest):
    return generar_contenido(solicitud)
