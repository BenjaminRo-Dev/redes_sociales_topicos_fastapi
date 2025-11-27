from pydantic import BaseModel, Field


class PublicarWhatsappRequest(BaseModel):
    texto: str
    url_img: str

