import requests
from app.core.config import Settings
from fastapi import HTTPException
from typing import Any, Dict

settings = Settings()


class FacebookService:

    def __init__(self):

        self.api_url: str | None = settings.FACEBOOK_API_URL
        self.token: str | None = settings.FACEBOOK_TOKEN

        self.id_pagina: str = getattr(settings, "FACEBOOK_ID_PAGINA", "me")

    def realizar_peticion(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.api_url}/{endpoint}"

        data["access_token"] = self.token

        try:
            respuesta = requests.post(url, data=data)
            respuesta.raise_for_status()
            return respuesta.json()

        except requests.exceptions.RequestException as e:
            status_code = (
                e.response.status_code
                if hasattr(e, "response") and e.response is not None
                else 500
            )
            raise HTTPException(
                status_code=status_code,
                detail=f"Error al publicar en Facebook: {e}",
            )

    def publicar_post(self, texto: str, url_img: str | None = None) -> Dict[str, Any]:
        if url_img:
            endpoint = f"{self.id_pagina}/photos"
            datos = {"caption": texto, "url": url_img}
        else:
            endpoint = f"{self.id_pagina}/feed"
            datos = {"message": texto}

        return self.realizar_peticion(endpoint, datos)


facebook_service = FacebookService()
