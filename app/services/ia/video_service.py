import os
import time
import base64
from typing import Optional

from app.core.config import settings
from google import genai
from google.genai import types

# Configuración de Gemini:
client = genai.Client()

VIDEOS_DIR = "app/static/videos/"


def __generar_video_con_gemini(
    prompt: str, 
    duration_seconds: int = 4,
    aspect_ratio: str = "9:16",
) -> dict:
    
    try:
        config_params = {
            "aspect_ratio": aspect_ratio,
            "number_of_videos": 1,
            "duration_seconds": duration_seconds
        }
        
        # Generar el video
        operation = client.models.generate_videos(
            # model="veo-3.1-generate-preview",
            model="veo-3.1-fast-generate-preview",
            prompt=prompt,
            config=types.GenerateVideosConfig(**config_params),
        )
        
        # Poll del estado de la operación hasta que el video esté listo
        while not operation.done:
            print("Esperando a que se complete la generación del video...")
            time.sleep(10)
            operation = client.operations.get(operation)
        
        # Obtener el video generado
        if operation.response and operation.response.generated_videos:
            video = operation.response.generated_videos[0]
            
            # Crear directorio si no existe
            os.makedirs(VIDEOS_DIR, exist_ok=True)
            
            # Generar nombre único para el video
            nombre_video = f"video_{hash(prompt)}_{int(time.time())}.mp4"
            ruta_video = os.path.join(VIDEOS_DIR, nombre_video)
            
            # Descargar y guardar el video
            if video.video:
                client.files.download(file=video.video)
                video.video.save(ruta_video)
            else:
                raise Exception("No se pudo obtener el archivo de video")
            
            url_video = f"static/videos/{nombre_video}"
            
            print(f"Video generado y guardado en: {ruta_video}")
            
            return {
                "url_video": url_video,
                "prompt": prompt,
                "ruta_completa": ruta_video
            }
        else:
            raise Exception("No se pudo generar el video")
            
    except Exception as e:
        print(f"Error al generar video con Gemini: {e}")
        raise


def generar_video(
    prompt: str, 
    duration_seconds: int = 5,
    aspect_ratio: str = "16:9",
) -> dict:
    
    provider = settings.AI_PROVIDER

    if provider == "gemini":
        return __generar_video_con_gemini(prompt, duration_seconds, aspect_ratio)
        # return __generar_video_con_gemini(prompt)
    elif provider == "openai":
        raise NotImplementedError("El proveedor OpenAI aún no está implementado para generación de videos")
    else:
        raise ValueError(f"Proveedor de IA desconocido: {provider}")
