from fastapi import APIRouter, Depends
from app.schemas.publicar_facebook_schema import PublicarFacebookRequest
from app.schemas.publicar_instagram_schema import PublicarInstagramRequest
from app.services.instagram_service import instagram_service
from app.services.facebook_service import facebook_service

router = APIRouter(prefix="/publicar", tags=["Publicar"])


@router.post("/facebook", response_model=dict)
def publicar_facebook(publicacion: PublicarFacebookRequest):
    return facebook_service.publicar_post(
        texto=publicacion.texto, url_img=publicacion.url_img
    )


@router.post("/instagram", response_model=dict)
def publicar_instagram(publicacion: PublicarInstagramRequest):
    return instagram_service.publicar_post(
        texto=publicacion.texto, url_img=publicacion.url_img
    )