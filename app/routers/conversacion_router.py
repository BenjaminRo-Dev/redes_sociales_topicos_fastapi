from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.controllers.conversacion_controller import ConversacionController
from app.schemas.conversacion_schema import (
    ConversacionCreate,
    ConversacionUpdate,
    ConversacionResponse,
    ConversacionConMensajesResponse,
    MensajeCreate,
    MensajeResponse
)
from app.core.database import get_session
from app.services.jwt_service import get_current_user

router = APIRouter(prefix="/conversaciones", tags=["Conversaciones"])


@router.post("/", response_model=ConversacionResponse, status_code=status.HTTP_201_CREATED)
def crear_conversacion(
    request: ConversacionCreate,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        conversacion = ConversacionController.crear_conversacion(
            session=session,
            titulo=request.titulo,
            usuario_id=usuario_id
        )
        return conversacion
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/", response_model=List[ConversacionResponse])
def obtener_todas_conversaciones(
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        conversaciones = ConversacionController.obtener_todas_conversaciones(
            session=session,
            usuario_id=usuario_id
        )
        return conversaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{conversacion_id}", response_model=ConversacionResponse)
def obtener_conversacion(
    conversacion_id: int,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        conversacion = ConversacionController.obtener_conversacion_por_id(
            session=session,
            conversacion_id=conversacion_id
        )
        if not conversacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversación con id {conversacion_id} no encontrada"
            )
        return conversacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{conversacion_id}/mensajes", response_model=List[MensajeResponse])
def obtener_mensajes_conversacion(
    conversacion_id: int,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        mensajes = ConversacionController.obtener_mensajes_conversacion(
            session=session,
            conversacion_id=conversacion_id
        )
        return mensajes
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/{conversacion_id}/mensajes", response_model=List[MensajeResponse], status_code=status.HTTP_201_CREATED)
def agregar_mensaje(
    conversacion_id: int,
    request: MensajeCreate,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        mensajes = ConversacionController.agregar_mensaje_con_ia(
            session=session,
            conversacion_id=conversacion_id,
            prompt_usuario=request.texto,
            redes_sociales=request.redes_sociales,
            duracion_video=request.duracion_video
        )
        return mensajes
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{conversacion_id}", response_model=ConversacionResponse)
def actualizar_conversacion(
    conversacion_id: int,
    request: ConversacionUpdate,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        conversacion = ConversacionController.actualizar_conversacion(
            session=session,
            conversacion_id=conversacion_id,
            titulo=request.titulo
        )
        if not conversacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversación con id {conversacion_id} no encontrada"
            )
        return conversacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{conversacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_conversacion(
    conversacion_id: int,
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        eliminado = ConversacionController.eliminar_conversacion(
            session=session,
            conversacion_id=conversacion_id
        )
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversación con id {conversacion_id} no encontrada"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/usuario/count", response_model=dict)
def contar_conversaciones_usuario(
    session: Session = Depends(get_session),
    usuario_id: int = Depends(get_current_user)
):
    try:
        cantidad = ConversacionController.contar_conversaciones_por_usuario(
            session=session,
            usuario_id=usuario_id
        )
        return {"usuario_id": usuario_id, "cantidad_conversaciones": cantidad}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
