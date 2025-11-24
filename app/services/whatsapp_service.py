from app.core.config import Settings
import requests
import base64
import os


settings = Settings()


class WhatsappService:

    def __init__(self):
        self.api_url: str | None = settings.WHATSAPP_API_URL
        self.token: str | None = settings.WHATSAPP_TOKEN

    def publicar_historia(self, imagen_url: str, texto: str) -> dict:
        # Extraer nombre del archivo de la URL
        nombre_imagen = os.path.basename(imagen_url)

        # Leer la imagen desde el archivo
        with open(imagen_url, "rb") as f:
            imagen_bytes = f.read()

        imagen_base64 = base64.b64encode(imagen_bytes).decode("utf-8")

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.token}",
            "content-type": "application/json",
        }

        datos = {
            "media": f"data:image/png;name={nombre_imagen};base64,{imagen_base64}",
            "caption": texto,
            "contacts": ["59176316283"],
        }

        response = requests.post(
            f"{self.api_url}/stories/send/media", headers=headers, json=datos
        )

        return response.json()


whatsapp_service = WhatsappService()
