from pydantic import BaseModel

class PublicarTiktokRequest(BaseModel):
    texto: str
    url_video: str
