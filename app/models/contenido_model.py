from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .tema_model import Tema
    from .archivo_model import Archivo
    from .redsocial_model import Redsocial

class Contenido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    publicado: bool = Field(default=True)
    fecha_publicacion: Optional[datetime] = None
    
    tema_id: int = Field(foreign_key="tema.id")
    redsocial_id: int = Field(foreign_key="redsocial.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
   
    # Relación: Un contenido pertenece a un tema
    tema: "Tema" = Relationship(back_populates="contenidos")
    # Relación: Un contenido pertenece a una red social
    redsocial: "Redsocial" = Relationship(back_populates="contenidos")
    # Relación: Un contenido contiene muchos archivos
    archivos: List["Archivo"] = Relationship(back_populates="contenido")