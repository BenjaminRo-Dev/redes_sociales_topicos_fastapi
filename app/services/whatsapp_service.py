from app.core.config import Settings
import requests
import base64
import os
from urllib.parse import urlparse


settings = Settings()


class WhatsappService:

    def __init__(self):
        self.api_url: str | None = settings.WHATSAPP_API_URL
        self.token: str | None = settings.WHATSAPP_TOKEN

    def publicar(self, texto: str, url_img: str) -> dict:
        response = requests.get(url_img)
        response.raise_for_status()
        imagen_bytes = response.content

        imagen_base64 = base64.b64encode(imagen_bytes).decode("utf-8")

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.token}",
            "content-type": "application/json",
        }

        datos = {
            "media": f"data:image/png;base64,{imagen_base64}",
            "caption": texto,
            "contacts": ["59176316283"],
        }

        response = requests.post(
            f"{self.api_url}/stories/send/media", headers=headers, json=datos
        )

        return response.json()


whatsapp_service = WhatsappService()
