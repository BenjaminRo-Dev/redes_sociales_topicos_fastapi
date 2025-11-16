from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.auth_schema import LoginRequest, Token

from app.core.database import get_session
from app.services.auth_service import autenticar_usuario

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=dict)
def login(data: LoginRequest, db: Session = Depends(get_session)):
    token = autenticar_usuario(db, data.email, data.password)
    return token
