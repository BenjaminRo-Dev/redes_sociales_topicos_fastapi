from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from app.models import *

# if TYPE_CHECKING:
#     from .tema_model import Tema

class Prompt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descripcion: str
    tema_id: int = Field(foreign_key="tema.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Un prompt pertenece a un tema
    tema: "Tema" = Relationship(back_populates="prompts")