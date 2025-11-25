from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArchivoCreateRequest(BaseModel):
    url: str
    prompt_text: Optional[str] = None


class ArchivoUpdateRequest(BaseModel):
    url: Optional[str] = None
    prompt_text: Optional[str] = None


class ArchivoResponse(BaseModel):
    id: int
    url: str
    prompt_text: Optional[str]
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True
