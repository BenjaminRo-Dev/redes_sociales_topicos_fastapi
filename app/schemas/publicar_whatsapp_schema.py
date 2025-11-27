from pydantic import BaseModel, Field


class PublicarWhatsappRequest(BaseModel):
    texto: str
    url_img: str
    
class PublicarWhatsappResponse(BaseModel):
    id: str = Field(..., description="ID de la publicación en WhatsApp")
    enlace: str = Field(..., description="Enlace directo a la publicación en WhatsApp")