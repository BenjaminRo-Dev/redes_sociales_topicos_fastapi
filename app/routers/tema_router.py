from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated, List
from app.controllers.tema_controller import TemaController
from app.schemas.tema_schema import (
    TemaCreateRequest,
    TemaUpdateRequest,
    TemaResponse,
    TemaHistorialResponse
)
from app.core.database import get_session
from app.services.jwt_service import get_current_user

router = APIRouter(prefix="/temas", tags=["Temas"])


@router.post("/", response_model=TemaResponse, status_code=status.HTTP_201_CREATED)
def crear_tema(
    request: TemaCreateRequest,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        tema = TemaController.crear_tema(
            session=session, nombre=request.nombre, usuario_id=usuario_id
        )
        return tema
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[TemaResponse])
def obtener_todos_temas(
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        temas = TemaController.obtener_todos_temas(session=session)
        return temas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{tema_id}", response_model=TemaResponse)
def obtener_tema(
    tema_id: int,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        tema = TemaController.obtener_tema_por_id(session=session, tema_id=tema_id)
        if not tema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tema con id {tema_id} no encontrado",
            )
        return tema
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{tema_id}/historial", response_model=TemaHistorialResponse)
def obtener_historial_tema(
    tema_id: int,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    """
    Obtiene el historial completo de un tema: todos sus prompts y contenidos
    ordenados cronológicamente para mostrar como un chat.
    """
    try:
        historial = TemaController.obtener_historial_tema(session=session, tema_id=tema_id)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tema con id {tema_id} no encontrado",
            )
        return historial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/usuario/mis-temas", response_model=List[TemaResponse])
def obtener_temas_por_usuario(
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        temas = TemaController.obtener_temas_por_usuario(
            session=session, usuario_id=usuario_id
        )
        return temas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{tema_id}", response_model=TemaResponse)
def actualizar_tema(
    tema_id: int,
    request: TemaUpdateRequest,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        tema = TemaController.actualizar_tema(
            session=session,
            tema_id=tema_id,
            nombre=request.nombre,
            usuario_id=usuario_id,
        )
        if not tema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tema con id {tema_id} no encontrado",
            )
        return tema
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{tema_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tema(
    tema_id: int,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        eliminado = TemaController.eliminar_tema(session=session, tema_id=tema_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tema con id {tema_id} no encontrado",
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/usuario/count", response_model=dict)
def contar_temas_usuario(
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        cantidad = TemaController.contar_temas_por_usuario(
            session=session, usuario_id=usuario_id
        )
        return {"usuario_id": usuario_id, "cantidad_temas": cantidad}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
