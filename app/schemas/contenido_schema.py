from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ContenidoCreateRequest(BaseModel):
    descripcion: str
    tema_id: int
    redsocial_id: int
    archivo_id: int
    publicado: bool = True
    fecha_publicacion: Optional[datetime] = None
    enlace_publicacion: Optional[str] = None


class ContenidoUpdateRequest(BaseModel):
    descripcion: Optional[str] = None
    publicado: Optional[bool] = None
    fecha_publicacion: Optional[datetime] = None
    enlace_publicacion: Optional[str] = None
    tema_id: Optional[int] = None
    redsocial_id: Optional[int] = None
    archivo_id: Optional[int] = None


class ContenidoResponse(BaseModel):
    id: int
    descripcion: str
    publicado: bool
    fecha_publicacion: Optional[datetime]
    enlace_publicacion: Optional[str]
    tema_id: int
    redsocial_id: int
    archivo_id: int
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True
