from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TemaCreateRequest(BaseModel):
    nombre: str


class TemaUpdateRequest(BaseModel):
    nombre: Optional[str] = None


class TemaResponse(BaseModel):
    id: int
    nombre: str
    usuario_id: int
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True
