from datetime import datetime, timedelta, timezone
from typing import Annotated

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

try:
    SECRET_KEY = str(settings.SECRET_KEY)
    ALGORITHM = str(settings.ALGORITHM)
    if settings.ACCESS_TOKEN_EXPIRE_MINUTES is None:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES no está configurado")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
except Exception as e:
    raise RuntimeError(f"Falta una variable en el archivo .env: {e}")

# Esquema de seguridad: le indica a FastAPI dónde buscar el token (Header de Autorización Bearer)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    """Genera un JWT de acceso con tiempo de expiración."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Firma el token usando la clave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    DEPENDENCIA: Decodifica el token para obtener los datos del usuario.
    Se inyecta en las rutas que necesitan protección.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Intenta decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # El sub (subject) es donde guardamos el ID de usuario
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        # Retornamos el ID de usuario verificado
        return user_id 

    except JWTError:
        # Si la firma es inválida o el token expiró, lanza la excepción
        raise credentials_exception