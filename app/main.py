from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from app.controllers import tema_controller
from app.core.database import init_db
from app.routers import archivo_router, chat_router, contenido_router, linkedin_router, login_router, prompt_router, publicar_router, redsocial_router, tema_router, tiktok_router, whatsapp_router
from app.services.jwt_service import get_current_user
from app.core.cors import configuracion_cors


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando app")
    init_db()
    yield
    print("Cerrando app")


app = FastAPI(
    title="Generador de contenido con LLM para redes sociales", lifespan=lifespan
)


configuracion_cors(app)
app.mount("/static", StaticFiles(directory="app/static/"), name="static")


@app.get("/")
def root(user_id: Annotated[int, Depends(get_current_user)]):
    return {"message": "'API Generador de contenido' funcionando"}


app.include_router(login_router.router)
app.include_router(chat_router.router)
app.include_router(publicar_router.router)
app.include_router(tiktok_router.router)
app.include_router(whatsapp_router.router)
app.include_router(linkedin_router.router)

app.include_router(tema_router.router)
app.include_router(prompt_router.router)
app.include_router(redsocial_router.router)
app.include_router(archivo_router.router)
app.include_router(contenido_router.router)
