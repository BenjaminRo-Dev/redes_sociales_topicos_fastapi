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
    prompt_imagen: Optional[str] = None
    prompt_video: Optional[str] = None
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


# Schema para crear un mensaje (solicitud del usuario)
class MensajeCreate(BaseModel):
    texto: str = Field(..., min_length=1, description="Prompt o solicitud del usuario")
    redes_sociales: list[str] = Field(default=["facebook", "instagram", "linkedin", "whatsapp", "tiktok"], description="Redes sociales para generar contenido")
    duracion_video: int = Field(default=4, description="Duración del video en segundos")
