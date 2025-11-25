from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RedsocialCreateRequest(BaseModel):
    nombre: str


class RedsocialUpdateRequest(BaseModel):
    nombre: Optional[str] = None


class RedsocialResponse(BaseModel):
    id: int
    nombre: str
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True
