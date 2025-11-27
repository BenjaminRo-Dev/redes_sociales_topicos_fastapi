from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Schema para crear una conversación
class ConversacionCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255, description="Título de la conversación")


# Schema para actualizar una conversación
class ConversacionUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=255, description="Título de la conversación")


# Schema para respuesta de mensaje
class MensajeResponse(BaseModel):
    id: int
    emisor: str
    texto: str
    red_social: Optional[str] = None
    url_archivo: Optional[str] = None
    publicado: bool
    url_publicacion: Optional[str] = None
    conversacion_id: int
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True


# Schema para respuesta de conversación
class ConversacionResponse(BaseModel):
    id: int
    titulo: str
    usuario_id: int
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True


# Schema para respuesta de conversación con mensajes
class ConversacionConMensajesResponse(BaseModel):
    id: int
    titulo: str
    usuario_id: int
    create_at: datetime
    update_at: datetime
    mensajes: list[MensajeResponse] = []
    
    class Config:
        from_attributes = True


# Schema para crear un mensaje
class MensajeCreate(BaseModel):
    emisor: str = Field(..., description="Emisor del mensaje (usuario o asistente)")
    texto: str = Field(..., min_length=1, description="Contenido del mensaje")
    red_social: Optional[str] = Field(None, description="Red social asociada")
    url_archivo: Optional[str] = Field(None, description="URL del archivo generado")
    publicado: bool = Field(default=False, description="Si el contenido fue publicado")
    url_publicacion: Optional[str] = Field(None, description="URL de la publicación")
