from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.publicar_linkedin_schema import PublicarLinkedinRequest
from app.services.linkedin_service import linkedin_service

router = APIRouter(prefix="/linkedin", tags=["Linkedin"])

@router.post("/publicar", response_model=dict)
def publicar(request: PublicarLinkedinRequest):
    return linkedin_service.publicar_imagen(request.imagen_ruta, request.texto)