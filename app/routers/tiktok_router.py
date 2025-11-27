from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Dict

from app.services.tiktok_oaut_service import TiktokOauthService
from app.services.tiktok_post_service import TiktokPostService


router = APIRouter(prefix="/tiktok", tags=["TikTok"])

tiktok_oauth_service = TiktokOauthService()
tiktok_post_service = TiktokPostService()


@router.get("/auth/login")
def login() -> RedirectResponse:
    """Inicia el flujo de autenticación OAuth2 con TikTok."""
    return tiktok_oauth_service.login()


@router.get("/auth/callback")
async def callback(request: Request) -> JSONResponse:
    """Callback para recibir el código de autorización de TikTok."""
    code = request.query_params.get("code") or ""
    state = request.query_params.get("state") or ""

    return await tiktok_oauth_service.intercambiar_codigo_por_token(code, state)

