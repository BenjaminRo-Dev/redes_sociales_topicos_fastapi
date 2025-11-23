from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from google import genai

from app.core.database import init_db
from app.routers import chat_router, login_router, publicar_router, tiktok_router
from app.services.ia import imagen_service, video_service
from app.services.jwt_service import get_current_user
from app.core.cors import configuracion_cors

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando app")
    init_db()
    yield
    print("Cerrando app")

app = FastAPI(
    title="Generador de contenido con LLM para redes sociales",
    lifespan=lifespan
)

configuracion_cors(app)
app.mount("/static", StaticFiles(directory="app/static/"), name="static")

@app.get("/")
def root(user_id: Annotated[int, Depends(get_current_user)]):
    return {"message": "'API Generador de contenido' funcionando"}


@app.get("/generar/imagen")
def generar_imagen(prompt: str):
    return imagen_service.generar_imagen(prompt)


@app.get("/generar/video")
def generar_video(
    prompt: str,
    aspect_ratio: str = "16:9",
    duration_seconds: int = 4,
    usar_referencias: bool = False
):
    reference_images = None
    
    if usar_referencias:
        try:
            # Cargar imágenes de referencia
            client = genai.Client()
            
            img1 = client.files.upload(
                file="app/static/referencias/escudo.png",
                config={
                    "mime_type": "image/png",
                    "display_name": "escudo.png"
                }
            )
            
            img2 = client.files.upload(
                file="app/static/referencias/modulo.jpg",
                config={
                    "mime_type": "image/jpeg",
                    "display_name": "modulo.jpg"
                }
            )
            
            reference_images = [img1, img2]
        except Exception as e:
            print(f"Error al cargar imágenes de referencia: {e}")
            # Continuar sin referencias si falla la carga
    
    return video_service.generar_video(
        prompt=prompt,
        reference_images=reference_images,
        aspect_ratio=aspect_ratio,
        duration_seconds=duration_seconds
    )


app.include_router(login_router.router)
app.include_router(chat_router.router)
app.include_router(publicar_router.router)
app.include_router(tiktok_router.router)

