from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import init_db
from app.routers import login_router

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

app.include_router(login_router.router)

@app.get("/")
def root():
    return {"message": "'API Generador de contenido' funcionando"}