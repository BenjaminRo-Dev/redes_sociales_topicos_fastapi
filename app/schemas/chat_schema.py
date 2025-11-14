from pydantic import BaseModel, Field
from typing import Dict

class ChatRequest(BaseModel):
    tema: str = Field(examples=["Nueva funcionalidad en nuestra plataforma"])
    prompt: str = Field(examples=["Hoy lanzamos una nueva característica..."])
    redes_sociales: list[str] = Field(examples=[["facebook", "instagram", "linkedin", "whatsapp", "tiktok"]])

class RedSocialResponse(BaseModel):
    texto: str
    hashtags: list[str]
    cant_caracteres: int
    tono: str
    # suggested_image_prompt: str | None = None

class ChatResponse(BaseModel):
    respuesta: Dict[str, RedSocialResponse]

class PromptRequest(BaseModel):
    prompt: str = Field(..., examples=["Generar un post sobre la nueva matrícula universitaria"])
