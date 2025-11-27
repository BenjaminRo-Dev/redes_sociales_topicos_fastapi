import requests
from app.core.config import Settings
from fastapi import HTTPException
from typing import Any, Dict

settings = Settings()


class InstagramService:

    def __init__(self):
        self.api_url: str | None = settings.INSTAGRAM_API_URL
        self.token: str | None = settings.INSTAGRAM_TOKEN
        self.id_pagina: str = getattr(settings, "INSTAGRAM_ID_CUENTA", "me")


    def realizar_peticion(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.api_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            respuesta = requests.post(url, data=data, headers=headers)
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
                detail=f"Error al publicar en Instagram: {e}",
            )


    def __obtener_permalink(self, media_id: str) -> str:
        url = f"{self.api_url}/{media_id}?fields=permalink"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            respuesta = requests.get(url, headers=headers)
            respuesta.raise_for_status()
            datos = respuesta.json()
            permalink = datos.get("permalink")

            if not permalink:
                raise HTTPException(
                    status_code=500, detail="No se recibió permalink de Instagram"
                )

            return permalink

        except requests.exceptions.RequestException as e:
            status_code = (
                e.response.status_code
                if hasattr(e, "response") and e.response is not None
                else 500
            )
            raise HTTPException(
                status_code=status_code,
                detail=f"Error al obtener permalink de Instagram: {e}",
            )


    def __crear_contenedor_media(
        self, image_url: str, caption: str | None = None
    ) -> str:
        endpoint = f"{self.id_pagina}/media"
        datos = {"image_url": image_url, "access_token": self.token}

        if caption:
            datos["caption"] = caption

        respuesta = self.realizar_peticion(endpoint, datos)
        creation_id = respuesta.get("id")
        if not creation_id:
            raise HTTPException(
                status_code=500, detail="No se recibió ID del contenedor de Instagram"
            )
        print("Creation ID Instagram:", creation_id)
        return creation_id


    def __publicar_contenedor(self, creation_id: str) -> Dict[str, Any]:
        endpoint = f"{self.id_pagina}/media_publish"
        datos = {"creation_id": creation_id, "access_token": self.token}
        print("Publicar contenedor Instagram datos:", datos)
        return self.realizar_peticion(endpoint, datos)


    def publicar_post(self, url_img: str, texto: str | None = None) -> Dict[str, Any]:
        creation_id = self.__crear_contenedor_media(url_img, texto)
        respuesta = self.__publicar_contenedor(creation_id)

        if "id" in respuesta:
            media_id = respuesta["id"]
            respuesta["enlace"] = self.__obtener_permalink(media_id)

        return respuesta


instagram_service = InstagramService()
