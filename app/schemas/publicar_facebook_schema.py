from pydantic import BaseModel

class PublicarFacebookRequest(BaseModel):
    texto: str
    url_img: str | None = None
