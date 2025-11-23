import os

from app.core.config import settings
from google import genai
from google.genai import types

# Configuración de Gemini:
client = genai.Client()

IMAGES_DIR = "app/static/images/"


def __generar_imagen_con_gemini(prompt: str) -> dict:
    try:
        respuesta = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                # image_size="1K",
                # aspect_ratio="19:9"
                # include_safety_attributes=True
            )
        )
        
        if respuesta and respuesta.generated_images:
            imagen_obj = respuesta.generated_images[0]
            
            if imagen_obj.image is None or imagen_obj.image.image_bytes is None:
                raise Exception("No se pudo obtener los datos de la imagen")
            
            imagen_bytes = imagen_obj.image.image_bytes
            
            os.makedirs(IMAGES_DIR, exist_ok=True)
            
            nombre_imagen = f"{IMAGES_DIR}imagen_{hash(prompt)}.png"
            ruta_imagen = os.path.join(nombre_imagen)
            
            #Guardar la imagen
            with open(ruta_imagen, "wb") as f:
                f.write(imagen_bytes)
            
            url_imagen = f"static/images/imagen_{hash(prompt)}.png"
            
            return {
                "url_imagen": url_imagen,
                "prompt": prompt,
                # "safety_attributes": getattr(imagen_obj, 'safety_attributes', None)
            }
        else:
            raise Exception("No se pudo generar la imagen")
            
    except Exception as e:
        print(f"Error al generar imagen con Gemini: {e}")
        raise


def generar_imagen(prompt: str) -> dict:
    provider = settings.AI_PROVIDER

    if provider == "gemini":
        return __generar_imagen_con_gemini(prompt)
    elif provider == "openai":
        raise NotImplementedError("El proveedor OpenAI aún no está implementado")
    else:
        raise ValueError(f"Proveedor de IA desconocido: {provider}")
