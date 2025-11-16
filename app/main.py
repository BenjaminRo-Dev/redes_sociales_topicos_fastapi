from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI

from app.core.database import init_db
from app.routers import chat_router, login_router
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

@app.get("/")
def root(user_id: Annotated[int, Depends(get_current_user)]):
    return {"message": "'API Generador de contenido' funcionando"}

app.include_router(login_router.router)
app.include_router(chat_router.router)

