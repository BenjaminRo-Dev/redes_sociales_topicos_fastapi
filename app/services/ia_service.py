import json

from fastapi.responses import JSONResponse
from app.core.config import settings
from google import genai
from google.genai import types

# Configuración de Gemini:
client = genai.Client()

def __generar_con_gemini(prompt: str, instrucciones: str) -> str:
    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=instrucciones
            ),
            contents=prompt
        )
        if respuesta and respuesta.text:
            return respuesta.text
        else:
            return "No se pudo obtener una respuesta desde GEMINI"
    except Exception as e:
        print(f"Error al generar contenido con Gemini: {e}")
        raise


def generar_contenido(prompt: str, instrucciones: str) -> str:
    provider = settings.AI_PROVIDER

    if provider == "gemini":
        return __generar_con_gemini(prompt, instrucciones)
    elif provider == "openai":
        raise NotImplementedError("El proveedor OpenAI aún no está implementado")
    else:
        raise ValueError(f"Proveedor de IA desconocido: {provider}")
