from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.controllers.contenido_controller import ContenidoController
from app.schemas.contenido_schema import ContenidoCreateRequest, ContenidoUpdateRequest, ContenidoResponse
from app.core.database import get_session
from typing import List

router = APIRouter(prefix="/contenidos", tags=["Contenidos"])


@router.post("/", response_model=ContenidoResponse, status_code=status.HTTP_201_CREATED)
def crear_contenido(request: ContenidoCreateRequest, session: Session = Depends(get_session)):
    """
    Crear un nuevo contenido
    """
    try:
        contenido = ContenidoController.crear_contenido(
            session=session,
            descripcion=request.descripcion,
            tema_id=request.tema_id,
            redsocial_id=request.redsocial_id,
            archivo_id=request.archivo_id,
            publicado=request.publicado,
            fecha_publicacion=request.fecha_publicacion,
            enlace_publicacion=request.enlace_publicacion
        )
        return contenido
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[ContenidoResponse])
def obtener_todos_contenidos(session: Session = Depends(get_session)):
    """
    Obtener todos los contenidos
    """
    try:
        contenidos = ContenidoController.obtener_todos_contenidos(session=session)
        return contenidos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{contenido_id}", response_model=ContenidoResponse)
def obtener_contenido(contenido_id: int, session: Session = Depends(get_session)):
    """
    Obtener un contenido por su ID
    """
    try:
        contenido = ContenidoController.obtener_contenido_por_id(
            session=session, contenido_id=contenido_id
        )
        if not contenido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contenido con id {contenido_id} no encontrado",
            )
        return contenido
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/tema/{tema_id}", response_model=List[ContenidoResponse])
def obtener_contenidos_por_tema(tema_id: int, session: Session = Depends(get_session)):
    """
    Obtener todos los contenidos de un tema específico
    """
    try:
        contenidos = ContenidoController.obtener_contenidos_por_tema(
            session=session, tema_id=tema_id
        )
        return contenidos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/redsocial/{redsocial_id}", response_model=List[ContenidoResponse])
def obtener_contenidos_por_redsocial(redsocial_id: int, session: Session = Depends(get_session)):
    """
    Obtener todos los contenidos de una red social específica
    """
    try:
        contenidos = ContenidoController.obtener_contenidos_por_redsocial(
            session=session, redsocial_id=redsocial_id
        )
        return contenidos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/publicados/{publicado}", response_model=List[ContenidoResponse])
def obtener_contenidos_publicados(publicado: bool, session: Session = Depends(get_session)):
    """
    Obtener contenidos filtrados por estado de publicación
    """
    try:
        contenidos = ContenidoController.obtener_contenidos_publicados(
            session=session, publicado=publicado
        )
        return contenidos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{contenido_id}", response_model=ContenidoResponse)
def actualizar_contenido(
    contenido_id: int, request: ContenidoUpdateRequest, session: Session = Depends(get_session)
):
    """
    Actualizar un contenido existente
    """
    try:
        contenido = ContenidoController.actualizar_contenido(
            session=session,
            contenido_id=contenido_id,
            descripcion=request.descripcion,
            publicado=request.publicado,
            fecha_publicacion=request.fecha_publicacion,
            enlace_publicacion=request.enlace_publicacion,
            tema_id=request.tema_id,
            redsocial_id=request.redsocial_id,
            archivo_id=request.archivo_id,
        )
        if not contenido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contenido con id {contenido_id} no encontrado",
            )
        return contenido
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{contenido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contenido(contenido_id: int, session: Session = Depends(get_session)):
    """
    Eliminar un contenido por su ID
    """
    try:
        eliminado = ContenidoController.eliminar_contenido(
            session=session, contenido_id=contenido_id
        )
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contenido con id {contenido_id} no encontrado",
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/tema/{tema_id}/count", response_model=dict)
def contar_contenidos_tema(tema_id: int, session: Session = Depends(get_session)):
    """
    Contar cuántos contenidos tiene un tema
    """
    try:
        cantidad = ContenidoController.contar_contenidos_por_tema(
            session=session, tema_id=tema_id
        )
        return {"tema_id": tema_id, "cantidad_contenidos": cantidad}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/redsocial/{redsocial_id}/count", response_model=dict)
def contar_contenidos_redsocial(redsocial_id: int, session: Session = Depends(get_session)):
    """
    Contar cuántos contenidos tiene una red social
    """
    try:
        cantidad = ContenidoController.contar_contenidos_por_redsocial(
            session=session, redsocial_id=redsocial_id
        )
        return {"redsocial_id": redsocial_id, "cantidad_contenidos": cantidad}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
