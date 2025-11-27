from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(index=True, unique=True)
    password: str
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Un usuario puede crear muchos temas
    temas: list["Conversacion"] = Relationship(back_populates="usuario")

class Conversacion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    usuario_id: int = Field(foreign_key="usuario.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relaciones
    usuario: Usuario = Relationship(back_populates="temas")
    mensajes: list["Mensaje"] = Relationship(back_populates="conversacion")

class Mensaje(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    emisor: str
    texto: str
    red_social: str | None = Field(default=None)
    url_archivo: str | None = Field(default=None)
    publicado: bool = Field(default=False)
    url_publicacion: str | None = Field(default=None)
    prompt_imagen: str | None = Field(default=None)
    prompt_video: str | None = Field(default=None)
    conversacion_id: int = Field(foreign_key="conversacion.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación
    conversacion: Conversacion = Relationship(back_populates="mensajes")