from sqlmodel import Session, select
from app.models.modelos import Prompt, Tema
from datetime import datetime, timezone
from typing import List, Optional


class PromptController:
    
    @staticmethod
    def crear_prompt(session: Session, descripcion: str, tema_id: int) -> Prompt:
        """
        Crear un nuevo prompt
        """
        # Verificar que el tema existe
        tema = session.get(Tema, tema_id)
        if not tema:
            raise ValueError(f"Tema con id {tema_id} no existe")
        
        nuevo_prompt = Prompt(
            descripcion=descripcion,
            tema_id=tema_id
        )
        session.add(nuevo_prompt)
        session.commit()
        session.refresh(nuevo_prompt)
        return nuevo_prompt
    
    
    @staticmethod
    def obtener_prompt_por_id(session: Session, prompt_id: int) -> Optional[Prompt]:
        """
        Obtener un prompt por su ID
        """
        prompt = session.get(Prompt, prompt_id)
        return prompt
    
    
    @staticmethod
    def obtener_todos_prompts(session: Session) -> List[Prompt]:
        """
        Obtener todos los prompts
        """
        statement = select(Prompt)
        prompts = session.exec(statement).all()
        return list(prompts)
    
    
    @staticmethod
    def obtener_prompts_por_tema(session: Session, tema_id: int) -> List[Prompt]:
        """
        Obtener todos los prompts de un tema específico
        """
        statement = select(Prompt).where(Prompt.tema_id == tema_id)
        prompts = session.exec(statement).all()
        return list(prompts)
    
    
    @staticmethod
    def actualizar_prompt(session: Session, prompt_id: int, descripcion: Optional[str] = None, 
                         tema_id: Optional[int] = None) -> Optional[Prompt]:
        """
        Actualizar un prompt existente
        """
        prompt = session.get(Prompt, prompt_id)
        if not prompt:
            return None
        
        # Actualizar campos si se proporcionan
        if descripcion is not None:
            prompt.descripcion = descripcion
        
        if tema_id is not None:
            # Verificar que el nuevo tema existe
            tema = session.get(Tema, tema_id)
            if not tema:
                raise ValueError(f"Tema con id {tema_id} no existe")
            prompt.tema_id = tema_id
        
        # Actualizar fecha de modificación
        prompt.update_at = datetime.now(timezone.utc)
        
        session.add(prompt)
        session.commit()
        session.refresh(prompt)
        return prompt
    
    
    @staticmethod
    def eliminar_prompt(session: Session, prompt_id: int) -> bool:
        """
        Eliminar un prompt por su ID
        """
        prompt = session.get(Prompt, prompt_id)
        if not prompt:
            return False
        
        session.delete(prompt)
        session.commit()
        return True
    
    
    @staticmethod
    def contar_prompts_por_tema(session: Session, tema_id: int) -> int:
        """
        Contar cuántos prompts tiene un tema
        """
        statement = select(Prompt).where(Prompt.tema_id == tema_id)
        prompts = session.exec(statement).all()
        return len(list(prompts))
