from fastapi import APIRouter, Depends
from app.schemas.publicar_facebook_schema import PublicarRequest
from app.services.facebook_service import facebook_service

router = APIRouter(prefix="/publicar", tags=["Publicar"])


@router.post("/facebook", response_model=dict)
def publicar_facebook(publicacion: PublicarRequest):
    return facebook_service.publicar_post(
        texto=publicacion.texto, url_img=publicacion.url_img
    )
