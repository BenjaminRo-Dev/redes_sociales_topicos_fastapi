from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.controllers.prompt_controller import PromptController
from app.schemas.prompt_schema import PromptCreateRequest, PromptUpdateRequest, PromptResponse
from app.core.database import get_session
from typing import List

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post("/", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
def crear_prompt(request: PromptCreateRequest, session: Session = Depends(get_session)):
    """
    Crear un nuevo prompt
    """
    try:
        prompt = PromptController.crear_prompt(
            session=session, descripcion=request.descripcion, tema_id=request.tema_id
        )
        return prompt
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[PromptResponse])
def obtener_todos_prompts(session: Session = Depends(get_session)):
    """
    Obtener todos los prompts
    """
    try:
        prompts = PromptController.obtener_todos_prompts(session=session)
        return prompts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{prompt_id}", response_model=PromptResponse)
def obtener_prompt(prompt_id: int, session: Session = Depends(get_session)):
    """
    Obtener un prompt por su ID
    """
    try:
        prompt = PromptController.obtener_prompt_por_id(session=session, prompt_id=prompt_id)
        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prompt con id {prompt_id} no encontrado",
            )
        return prompt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/tema/{tema_id}", response_model=List[PromptResponse])
def obtener_prompts_por_tema(tema_id: int, session: Session = Depends(get_session)):
    """
    Obtener todos los prompts de un tema específico
    """
    try:
        prompts = PromptController.obtener_prompts_por_tema(
            session=session, tema_id=tema_id
        )
        return prompts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{prompt_id}", response_model=PromptResponse)
def actualizar_prompt(
    prompt_id: int, request: PromptUpdateRequest, session: Session = Depends(get_session)
):
    """
    Actualizar un prompt existente
    """
    try:
        prompt = PromptController.actualizar_prompt(
            session=session,
            prompt_id=prompt_id,
            descripcion=request.descripcion,
            tema_id=request.tema_id,
        )
        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prompt con id {prompt_id} no encontrado",
            )
        return prompt
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_prompt(prompt_id: int, session: Session = Depends(get_session)):
    """
    Eliminar un prompt por su ID
    """
    try:
        eliminado = PromptController.eliminar_prompt(session=session, prompt_id=prompt_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prompt con id {prompt_id} no encontrado",
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/tema/{tema_id}/count", response_model=dict)
def contar_prompts_tema(tema_id: int, session: Session = Depends(get_session)):
    """
    Contar cuántos prompts tiene un tema
    """
    try:
        cantidad = PromptController.contar_prompts_por_tema(
            session=session, tema_id=tema_id
        )
        return {"tema_id": tema_id, "cantidad_prompts": cantidad}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
