from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ContentResponse
from app.services.chat_service import generar_contenido

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/generar", response_model=ContentResponse)
def generar_contenido_redsocial(data: ChatRequest):
    return generar_contenido(data)
