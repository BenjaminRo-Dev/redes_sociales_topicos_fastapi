from typing import Dict
from fastapi import APIRouter
from app.schemas.publicar_facebook_schema import PublicarFacebookRequest, PublicarFacebookResponse
from app.schemas.publicar_instagram_schema import PublicarInstagramRequest, PublicarInstagramResponse
from app.schemas.publicar_linkedin_schema import PublicarLinkedinRequest
from app.services.tiktok_post_service import TiktokPostService
from app.services.whatsapp_service import whatsapp_service
from app.services.linkedin_service import linkedin_service
from app.services.instagram_service import instagram_service
from app.services.facebook_service import facebook_service

tiktok_post_service = TiktokPostService()

router = APIRouter(prefix="/publicar", tags=["Publicar"])


@router.post("/facebook", response_model=PublicarFacebookResponse)
def publicar_facebook(publicacion: PublicarFacebookRequest):
    return facebook_service.publicar_post(
        texto=publicacion.texto, url_img=publicacion.url_img
    )


@router.post("/instagram", response_model=PublicarInstagramResponse)
def publicar_instagram(publicacion: PublicarInstagramRequest):
    return instagram_service.publicar_post(
        texto=publicacion.texto, url_img=publicacion.url_img
    )
    
    
@router.post("/linkedin", response_model=dict)
def publicar_linkedin(request: PublicarLinkedinRequest):
    return linkedin_service.publicar_imagen(request.imagen_ruta, request.texto)


@router.post("/whatsapp", response_model=dict)
def publicar_historia(imagen_url: str, texto: str):
    return whatsapp_service.publicar_historia(imagen_url=imagen_url, texto=texto)


@router.post("/tiktok", response_model=dict)
async def publicar_video(texto: str, video_url: str) -> Dict[str, str | Dict]:
    return await tiktok_post_service.publicar_video(texto, video_url)
