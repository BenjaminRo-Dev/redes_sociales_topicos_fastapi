from passlib.context import CryptContext
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.models.usuario_model import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password_texto: str, password_hasheado: str) -> bool:
    return pwd_context.verify(password_texto, password_hasheado)

def obtener_usuario(session: Session, email: str) -> Usuario | None:
    statement = select(Usuario).where(Usuario.email == email)
    result = session.exec(statement).first()
    return result

def autenticar_usuario(session: Session, email: str, password: str) -> Usuario:
    usuario = obtener_usuario(session, email)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    if not verificar_password(password, usuario.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    return usuario
