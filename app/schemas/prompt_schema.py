from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PromptCreateRequest(BaseModel):
    descripcion: str
    tema_id: int


class PromptUpdateRequest(BaseModel):
    descripcion: Optional[str] = None
    tema_id: Optional[int] = None


class PromptResponse(BaseModel):
    id: int
    descripcion: str
    tema_id: int
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True
