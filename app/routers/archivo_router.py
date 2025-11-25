from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.controllers.archivo_controller import ArchivoController
from app.schemas.archivo_schema import ArchivoCreateRequest, ArchivoUpdateRequest, ArchivoResponse
from app.core.database import get_session
from typing import List

router = APIRouter(prefix="/archivos", tags=["Archivos"])


@router.post("/", response_model=ArchivoResponse, status_code=status.HTTP_201_CREATED)
def crear_archivo(request: ArchivoCreateRequest, session: Session = Depends(get_session)):
    """
    Crear un nuevo archivo
    """
    try:
        archivo = ArchivoController.crear_archivo(
            session=session, url=request.url, prompt_text=request.prompt_text
        )
        return archivo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[ArchivoResponse])
def obtener_todos_archivos(session: Session = Depends(get_session)):
    """
    Obtener todos los archivos
    """
    try:
        archivos = ArchivoController.obtener_todos_archivos(session=session)
        return archivos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{archivo_id}", response_model=ArchivoResponse)
def obtener_archivo(archivo_id: int, session: Session = Depends(get_session)):
    """
    Obtener un archivo por su ID
    """
    try:
        archivo = ArchivoController.obtener_archivo_por_id(
            session=session, archivo_id=archivo_id
        )
        if not archivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Archivo con id {archivo_id} no encontrado",
            )
        return archivo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/contenido/{contenido_id}", response_model=ArchivoResponse)
def obtener_archivo_por_contenido(contenido_id: int, session: Session = Depends(get_session)):
    """
    Obtener el archivo de un contenido específico
    """
    try:
        archivo = ArchivoController.obtener_archivos_por_contenido(
            session=session, contenido_id=contenido_id
        )
        if not archivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró archivo para el contenido {contenido_id}",
            )
        return archivo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{archivo_id}", response_model=ArchivoResponse)
def actualizar_archivo(
    archivo_id: int, request: ArchivoUpdateRequest, session: Session = Depends(get_session)
):
    """
    Actualizar un archivo existente
    """
    try:
        archivo = ArchivoController.actualizar_archivo(
            session=session,
            archivo_id=archivo_id,
            url=request.url,
            prompt_text=request.prompt_text,
        )
        if not archivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Archivo con id {archivo_id} no encontrado",
            )
        return archivo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{archivo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_archivo(archivo_id: int, session: Session = Depends(get_session)):
    """
    Eliminar un archivo por su ID
    """
    try:
        eliminado = ArchivoController.eliminar_archivo(
            session=session, archivo_id=archivo_id
        )
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Archivo con id {archivo_id} no encontrado",
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/stats/count", response_model=dict)
def contar_archivos(session: Session = Depends(get_session)):
    """
    Contar cuántos archivos hay en total
    """
    try:
        cantidad = ArchivoController.contar_archivos_sin_contenido(session=session)
        return {"cantidad_archivos": cantidad}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
