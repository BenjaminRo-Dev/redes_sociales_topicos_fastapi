from pydantic import BaseModel, Field
from typing import Dict

class ChatRequest(BaseModel):
    prompt: str = Field(examples=["Hoy lanzamos una nueva característica..."])
    redes_sociales: list[str] = Field(examples=[["facebook", "instagram", "linkedin", "whatsapp", "tiktok"]])
    
