from passlib.context import CryptContext
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.schemas.chat_schema import ChatRequest, RedSocialResponse, ChatResponse
from app.services import ia_service

def generar_contenido(data: ChatRequest) -> ChatResponse:
    respuesta = {}
    
    for red_social in data.redes_sociales:
        texto = f"Generando contenido para {red_social} sobre el tema '{data.tema}' con el prompt: {data.prompt}"
        hashtags = [f"#{data.tema.replace(' ', '')}", f"#{red_social}"]
        cant_caracteres = len(texto)
        tono = "Informativo"
        
        chat_response = RedSocialResponse(
            texto=texto,
            hashtags=hashtags,
            cant_caracteres=cant_caracteres,
            tono=tono
        )
        
        respuesta[red_social] = chat_response

    return ChatResponse(respuesta=respuesta)

def generar_contenido_prueba(data: str) -> str:
    return ia_service.generar_contenido(data)
    