from pydantic import BaseModel

class PublicarInstagramRequest(BaseModel):
    texto: str | None
    url_img: str
