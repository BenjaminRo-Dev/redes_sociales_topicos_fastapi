from pydantic import BaseModel, Field
from typing import Dict

class ChatRequest(BaseModel):
    prompt: str
    duracion_video: int = 4
    redes_sociales: list[str] = Field(examples=[["facebook", "instagram", "linkedin", "whatsapp", "tiktok"]])
    
