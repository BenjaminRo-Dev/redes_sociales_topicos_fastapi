from pydantic import BaseModel, Field
from typing import Dict

class PublicarRequest(BaseModel):
    texto: str
    url_img: str | None = None
