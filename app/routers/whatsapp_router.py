from fastapi import APIRouter
from app.services.whatsapp_service import whatsapp_service

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])

@router.post("/publicar-historia", response_model=dict)
def publicar_historia(imagen_url: str, texto: str):
    return whatsapp_service.publicar_historia(imagen_url=imagen_url, texto=texto)