from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.controllers.tema_controller import TemaController
from app.schemas.tema_schema import TemaCreateRequest, TemaUpdateRequest, TemaResponse
from app.core.database import get_session
from typing import List

router = APIRouter(prefix="/temas", tags=["Temas"])


@router.post("/", response_model=TemaResponse, status_code=status.HTTP_201_CREATED)
def crear_tema(request: TemaCreateRequest, session: Session = Depends(get_session)):
    try:
        tema = TemaController.crear_tema(
            session=session, nombre=request.nombre, usuario_id=request.usuario_id
        )
        return tema
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[TemaResponse])
def obtener_todos_temas(session: Session = Depends(get_session)):
    try:
        temas = TemaController.obtener_todos_temas(session=session)
        return temas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{tema_id}", response_model=TemaResponse)
def obtener_tema(tema_id: int, session: Session = Depends(get_session)):
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


@router.get("/usuario/{usuario_id}", response_model=List[TemaResponse])
def obtener_temas_por_usuario(usuario_id: int, session: Session = Depends(get_session)):
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
    tema_id: int, request: TemaUpdateRequest, session: Session = Depends(get_session)
):
    try:
        tema = TemaController.actualizar_tema(
            session=session,
            tema_id=tema_id,
            nombre=request.nombre,
            usuario_id=request.usuario_id,
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
def eliminar_tema(tema_id: int, session: Session = Depends(get_session)):
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


@router.get("/usuario/{usuario_id}/count", response_model=dict)
def contar_temas_usuario(usuario_id: int, session: Session = Depends(get_session)):
    try:
        cantidad = TemaController.contar_temas_por_usuario(
            session=session, usuario_id=usuario_id
        )
        return {"usuario_id": usuario_id, "cantidad_temas": cantidad}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
