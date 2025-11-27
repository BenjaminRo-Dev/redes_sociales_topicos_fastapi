from pydantic import BaseModel, Field


class PublicarLinkedinRequest(BaseModel):
    texto: str
    url_img: str
    
class PublicarLinkedinResponse(BaseModel):
    id: str = Field(..., description="ID de la publicación en LinkedIn")
    enlace: str = Field(..., description="Enlace directo a la publicación en LinkedIn")