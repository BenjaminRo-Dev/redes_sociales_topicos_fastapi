
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from app.services.tiktok_oaut_service import TiktokOauthService

router = APIRouter()
tiktok_service = TiktokOauthService()

@router.get("/auth/tiktok/login")
def login() -> RedirectResponse:
    return tiktok_service.login()

@router.get("/auth/tiktok/callback")
async def callback(request: Request) -> JSONResponse:
    code = request.query_params.get("code") or ""
    state = request.query_params.get("state") or ""
    
    return await tiktok_service.intercambiar_codigo_por_token(code, state)
