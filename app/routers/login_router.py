from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session
from app.schemas.auth_schema import LoginRequest, LoginResponse

from app.core.database import get_session
from app.services.auth_service import autenticar_usuario

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_session)):
    usuario = autenticar_usuario(db, data.email, data.password)
    # TODO: GUARDAR sesión/token
    return {"id": usuario.id, "email": usuario.email, "message": "Autenticado"}
