from fastapi import UploadFile
from pydantic import BaseModel

class PublicarTiktokRequest(BaseModel):
    texto: str
    video: UploadFile
