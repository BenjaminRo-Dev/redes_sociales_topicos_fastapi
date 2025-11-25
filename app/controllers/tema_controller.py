from sqlmodel import Session, select, desc
from app.models.modelos import Tema, Usuario
from datetime import datetime, timezone
from typing import List, Optional


class TemaController:
    
    @staticmethod
    def crear_tema(session: Session, nombre: str, usuario_id: int) -> Tema:
        
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError(f"Usuario con id {usuario_id} no existe")
        
        nuevo_tema = Tema(
            nombre=nombre,
            usuario_id=usuario_id
        )
        session.add(nuevo_tema)
        session.commit()
        session.refresh(nuevo_tema)
        return nuevo_tema
    
    
    @staticmethod
    def obtener_tema_por_id(session: Session, tema_id: int) -> Optional[Tema]:
        tema = session.get(Tema, tema_id)
        return tema
    
    
    @staticmethod
    def obtener_todos_temas(session: Session) -> List[Tema]:
        statement = select(Tema).order_by(desc(Tema.update_at))
        temas = session.exec(statement).all()
        return list(temas)
    
    
    @staticmethod
    def obtener_temas_por_usuario(session: Session, usuario_id: int) -> List[Tema]:
        statement = select(Tema).where(Tema.usuario_id == usuario_id)
        temas = session.exec(statement).all()
        return list(temas)
    
    
    @staticmethod
    def actualizar_tema(session: Session, tema_id: int, nombre: Optional[str] = None, 
                       usuario_id: Optional[int] = None) -> Optional[Tema]:
        tema = session.get(Tema, tema_id)
        if not tema:
            return None
        
        # Actualizar campos si se proporcionan
        if nombre is not None:
            tema.nombre = nombre
        
        if usuario_id is not None:
            # Verificar que el nuevo usuario existe
            usuario = session.get(Usuario, usuario_id)
            if not usuario:
                raise ValueError(f"Usuario con id {usuario_id} no existe")
            tema.usuario_id = usuario_id
        
        # Actualizar fecha de modificación
        tema.update_at = datetime.now(timezone.utc)
        
        session.add(tema)
        session.commit()
        session.refresh(tema)
        return tema
    
    @staticmethod
    def eliminar_tema(session: Session, tema_id: int) -> bool:
        """
        Eliminar un tema por su ID
        """
        tema = session.get(Tema, tema_id)
        if not tema:
            return False
        
        session.delete(tema)
        session.commit()
        return True
    
    
    @staticmethod
    def contar_temas_por_usuario(session: Session, usuario_id: int) -> int:
        statement = select(Tema).where(Tema.usuario_id == usuario_id)
        temas = session.exec(statement).all()
        return len(list(temas))
