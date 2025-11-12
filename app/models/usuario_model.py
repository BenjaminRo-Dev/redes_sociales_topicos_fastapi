from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import table
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .tema_model import Tema

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(index=True, unique=True)
    password: str
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Un usuario puede crear muchos temas
    temas: List["Tema"] = Relationship(back_populates="usuario")