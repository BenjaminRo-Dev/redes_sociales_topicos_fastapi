from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.controllers.redsocial_controller import RedsocialController
from app.schemas.redsocial_schema import RedsocialCreateRequest, RedsocialUpdateRequest, RedsocialResponse
from app.core.database import get_session
from typing import List

router = APIRouter(prefix="/redsociales", tags=["Redes Sociales"])


@router.post("/", response_model=RedsocialResponse, status_code=status.HTTP_201_CREATED)
def crear_redsocial(request: RedsocialCreateRequest, session: Session = Depends(get_session)):
    """
    Crear una nueva red social
    """
    try:
        redsocial = RedsocialController.crear_redsocial(
            session=session, nombre=request.nombre
        )
        return redsocial
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[RedsocialResponse])
def obtener_todas_redsociales(session: Session = Depends(get_session)):
    """
    Obtener todas las redes sociales
    """
    try:
        redsociales = RedsocialController.obtener_todas_redsociales(session=session)
        return redsociales
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{redsocial_id}", response_model=RedsocialResponse)
def obtener_redsocial(redsocial_id: int, session: Session = Depends(get_session)):
    """
    Obtener una red social por su ID
    """
    try:
        redsocial = RedsocialController.obtener_redsocial_por_id(
            session=session, redsocial_id=redsocial_id
        )
        if not redsocial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Red social con id {redsocial_id} no encontrada",
            )
        return redsocial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/nombre/{nombre}", response_model=RedsocialResponse)
def obtener_redsocial_por_nombre(nombre: str, session: Session = Depends(get_session)):
    """
    Obtener una red social por su nombre
    """
    try:
        redsocial = RedsocialController.obtener_redsocial_por_nombre(
            session=session, nombre=nombre
        )
        if not redsocial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Red social con nombre '{nombre}' no encontrada",
            )
        return redsocial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{redsocial_id}", response_model=RedsocialResponse)
def actualizar_redsocial(
    redsocial_id: int, request: RedsocialUpdateRequest, session: Session = Depends(get_session)
):
    """
    Actualizar una red social existente
    """
    try:
        redsocial = RedsocialController.actualizar_redsocial(
            session=session,
            redsocial_id=redsocial_id,
            nombre=request.nombre,
        )
        if not redsocial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Red social con id {redsocial_id} no encontrada",
            )
        return redsocial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{redsocial_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_redsocial(redsocial_id: int, session: Session = Depends(get_session)):
    """
    Eliminar una red social por su ID
    """
    try:
        eliminado = RedsocialController.eliminar_redsocial(
            session=session, redsocial_id=redsocial_id
        )
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Red social con id {redsocial_id} no encontrada",
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/stats/count", response_model=dict)
def contar_redsociales(session: Session = Depends(get_session)):
    """
    Contar cuántas redes sociales hay registradas
    """
    try:
        cantidad = RedsocialController.contar_redsociales(session=session)
        return {"cantidad_redsociales": cantidad}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
