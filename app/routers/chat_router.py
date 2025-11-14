from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse, PromptRequest
from app.services.chat_service import generar_contenido, generar_contenido_prueba

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/generar", response_model=ChatResponse)
def generar_contenido_redsocial(data: ChatRequest):
    return generar_contenido(data)


@router.post("/prueba")
def prueba_ia(data: PromptRequest):
    resultado = generar_contenido_prueba(data.prompt)
    return {"contenido": resultado}