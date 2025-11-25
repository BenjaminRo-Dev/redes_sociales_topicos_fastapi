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
    temas: list["Tema"] = Relationship(back_populates="usuario")


class Tema(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    usuario_id: int = Field(foreign_key="usuario.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Un tema pertenece a un usuario
    usuario: "Usuario" = Relationship(back_populates="temas")
    prompts: list["Prompt"] = Relationship(back_populates="tema")
    contenidos: list["Contenido"] = Relationship(back_populates="tema")
    
    
class Prompt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descripcion: str
    tema_id: int = Field(foreign_key="tema.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Un prompt pertenece a un tema
    tema: "Tema" = Relationship(back_populates="prompts")
    
    
class Redsocial(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Una red social publica muchos contenidos
    contenidos: list["Contenido"] = Relationship(back_populates="redsocial")
    
    
class Contenido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descripcion: str
    publicado: bool = Field(default=True)
    fecha_publicacion: datetime | None = None
    enlace_publicacion: str | None = None
    
    tema_id: int = Field(foreign_key="tema.id")
    redsocial_id: int = Field(foreign_key="redsocial.id")
    archivo_id: int = Field(foreign_key="archivo.id")
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
   
    # Relación: Un contenido pertenece a un tema
    tema: "Tema" = Relationship(back_populates="contenidos")
    # Relación: Un contenido pertenece a una red social
    redsocial: "Redsocial" = Relationship(back_populates="contenidos")
    # Relación: Un contenido tiene un archivo
    archivo: "Archivo" = Relationship(back_populates="contenidos")
    

class Archivo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    prompt_text: str | None = None
    
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relación: Un archivo puede pertenecer a muchos contenidos
    contenidos: list["Contenido"] = Relationship(back_populates="archivo")
