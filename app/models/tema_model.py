from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .usuario_model import Usuario
    from .prompt_model import Prompt
    from .contenido_model import Contenido

class Tema(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    usuario_id: int = Field(foreign_key="usuario.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Un tema pertenece a un usuario
    usuario: "Usuario" = Relationship(back_populates="temas")
    prompts: List["Prompt"] = Relationship(back_populates="tema")
    contenidos: List["Contenido"] = Relationship(back_populates="tema")