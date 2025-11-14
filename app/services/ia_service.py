from app.core.config import settings
from google import genai
from google.genai import types

#Configuración de Gemini:
client = genai.Client()

instrucciones: str = ("Sos un asistente que solamente se dedica a generar el contenido referente a lo academico que se"
                      " publicará en redes sociales de la administracion de la 'Facultad de computación - FICCT'"
                      " de la UAGRM en Santa Cruz, Bolivia."
                      "- Longiitud de la respuesta: corta (si no se especifica),"
                      "- Responde directamente y solamente el contenido para pegar y copiar"
                      )

def __generarConGemini(prompt: str) -> str:
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


def generar_contenido(prompt: str) -> str:
    """Genera contenido usando IA."""
    provider = settings.AI_PROVIDER

    if provider == "gemini":
        return __generarConGemini(prompt)

    elif provider == "openai":
        raise NotImplementedError("El proveedor OpenAI aún no está implementado")
    else:
        raise ValueError(f"Proveedor de IA desconocido: {provider}")

