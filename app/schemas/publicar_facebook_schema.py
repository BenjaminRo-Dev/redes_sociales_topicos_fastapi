from pydantic import BaseModel, Field

class PublicarFacebookRequest(BaseModel):
    texto: str
    url_img: str | None = None


class PublicarFacebookResponse(BaseModel):
    id: str = Field(..., description="ID de la publicación")
    post_id: str | None = Field(None, description="ID completo del post (página_id_post_id)")
    enlace: str = Field(..., description="Enlace directo a la publicación en Facebook")
