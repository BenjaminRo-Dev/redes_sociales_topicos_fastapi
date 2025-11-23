from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest
from app.services.chat_service import generar_contenido
from app.services.ia import imagen_service, video_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/generar", response_model=dict)
def obtener_contenido(solicitud: ChatRequest):
    return generar_contenido(solicitud)


@router.post("/generar/imagen")
def generar_imagen(prompt: str):
    return imagen_service.generar_imagen(prompt)


@router.post("/generar/video")
def generar_video(prompt: str, duracion_segs: int = 4):

    return video_service.generar_video(prompt=prompt, duration_seconds=duracion_segs)
