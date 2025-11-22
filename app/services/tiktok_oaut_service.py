import secrets
from urllib.parse import urlencode
from typing import Dict

import httpx
from fastapi import HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from app.core.config import Settings


settings = Settings()


class TiktokOauthService:

    def __init__(self):
        self.client: str = settings.TIKTOK_CLIENT_KEY or ""
        self.secret: str = settings.TIKTOK_CLIENT_SECRET or ""
        self.callback: str = settings.TIKTOK_REDIRECT_URI or ""
        self.access_token: str | None = settings.TIKTOK_ACCESS_TOKEN
        self.open_id: str | None = settings.TIKTOK_OPEN_ID
        self.auth_url: str = settings.TIKTOK_AUTH_URL or "https://www.tiktok.com/v2/auth/authorize"
        self.token_url: str = settings.TIKTOK_TOKEN_URL or "https://open.tiktokapis.com/v2/oauth/token/"
        self.permisos: str = "user.info.basic"

        self._estado_store: Dict[str, str] = {}
        self._token_store: Dict[str, dict] = {}


    def login(self) -> RedirectResponse:
        estado = secrets.token_urlsafe(32)
        self._estado_store[estado] = "pending"

        parametros = {
            "response_type": "code",
            "client_key": self.client,
            "redirect_uri": self.callback,
            "scope": self.permisos,
            "state": estado,
        }

        query = urlencode(parametros)
        url = f"{self.auth_url}?{query}"
        return RedirectResponse(url)


    async def intercambiar_codigo_por_token(self, code: str, state: str) -> JSONResponse:
        if not code or not state:
            raise HTTPException(status_code=400, detail="Falta el código o el estado en la petición")

        if not self._existe_estado(state):
            raise HTTPException(status_code=400, detail="Estado inválido o expirado")

        data = {
            "client_key": self.client,
            "client_secret": self.secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.callback,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with httpx.AsyncClient() as client:
            respuesta = await client.post(self.token_url, data=data, headers=headers, timeout=20.0)

        if respuesta.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Error al intercambiar el código por token: {respuesta.text}",)

        token_resp = respuesta.json()
        user_open_id = token_resp.get("open_id")

        # Almacenar el token para el usuario
        self._token_store[user_open_id] = token_resp

        # Eliminar el estado usado
        self._eliminar_estado(state)

        return JSONResponse(
            {
                "status": "ok",
                "open_id": user_open_id,
                "access_token": token_resp.get("access_token"),
                "refresh_token": token_resp.get("refresh_token"),
                "expires_in": token_resp.get("expires_in"),
                "scope": token_resp.get("scope"),
            }
        )


    def obtener_token(self, open_id: str) -> dict | None:
        """Obtiene el token almacenado para un usuario específico."""
        return self._token_store.get(open_id)

    def _existe_estado(self, estado: str) -> bool:
        return estado in self._estado_store

    def _eliminar_estado(self, estado: str) -> None:
        if estado in self._estado_store:
            del self._estado_store[estado]
