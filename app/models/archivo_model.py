from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .contenido_model import Contenido

class Archivo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    
    contenido_id: int = Field(foreign_key="contenido.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Un archivo pertenece a un contenido
    contenido: "Contenido" = Relationship(back_populates="archivos")