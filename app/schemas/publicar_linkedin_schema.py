from pydantic import BaseModel


class PublicarLinkedinRequest(BaseModel):
    imagen_ruta: str  # ej: "app/static/images/imagen.png"
    texto: str