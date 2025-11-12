from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .contenido_model import Contenido

class Redsocial(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Una red social publica muchos contenidos
    contenidos: List["Contenido"] = Relationship(back_populates="redsocial")