from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Literal


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


class PromptHistorialItem(BaseModel):
    tipo: Literal["prompt"]
    id: int
    descripcion: str
    tema_id: int
    create_at: datetime
    update_at: datetime


class ContenidoHistorialItem(BaseModel):
    tipo: Literal["contenido"]
    id: int
    descripcion: str
    publicado: bool
    fecha_publicacion: Optional[datetime]
    enlace_publicacion: Optional[str]
    tema_id: int
    redsocial_id: int
    redsocial_nombre: Optional[str]
    archivo_id: int
    archivo_url: Optional[str]
    archivo_prompt_text: Optional[str]
    create_at: datetime
    update_at: datetime


class TemaHistorialResponse(BaseModel):
    tema_id: int
    tema_nombre: str
    usuario_id: int
    historial: List[PromptHistorialItem | ContenidoHistorialItem]
