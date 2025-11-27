from pydantic import BaseModel, Field

class PublicarInstagramRequest(BaseModel):
    texto: str | None
    url_img: str


class PublicarInstagramResponse(BaseModel):
    id: str = Field(..., description="ID de la publicación en Instagram")
    enlace: str = Field(..., description="Enlace directo a la publicación en Instagram")
