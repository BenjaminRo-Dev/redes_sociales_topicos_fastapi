from sqlmodel import Session, select
from app.models.modelos import Redsocial
from datetime import datetime, timezone
from typing import List, Optional


class RedsocialController:
    
    @staticmethod
    def crear_redsocial(session: Session, nombre: str) -> Redsocial:
        """
        Crear una nueva red social
        """
        nueva_redsocial = Redsocial(nombre=nombre)
        session.add(nueva_redsocial)
        session.commit()
        session.refresh(nueva_redsocial)
        return nueva_redsocial
    
    
    @staticmethod
    def obtener_redsocial_por_id(session: Session, redsocial_id: int) -> Optional[Redsocial]:
        """
        Obtener una red social por su ID
        """
        redsocial = session.get(Redsocial, redsocial_id)
        return redsocial
    
    
    @staticmethod
    def obtener_todas_redsociales(session: Session) -> List[Redsocial]:
        """
        Obtener todas las redes sociales
        """
        statement = select(Redsocial)
        redsociales = session.exec(statement).all()
        return list(redsociales)
    
    
    @staticmethod
    def obtener_redsocial_por_nombre(session: Session, nombre: str) -> Optional[Redsocial]:
        """
        Obtener una red social por su nombre
        """
        statement = select(Redsocial).where(Redsocial.nombre == nombre)
        redsocial = session.exec(statement).first()
        return redsocial
    
    
    @staticmethod
    def actualizar_redsocial(session: Session, redsocial_id: int, nombre: Optional[str] = None) -> Optional[Redsocial]:
        """
        Actualizar una red social existente
        """
        redsocial = session.get(Redsocial, redsocial_id)
        if not redsocial:
            return None
        
        # Actualizar campos si se proporcionan
        if nombre is not None:
            redsocial.nombre = nombre
        
        # Actualizar fecha de modificación
        redsocial.update_at = datetime.now(timezone.utc)
        
        session.add(redsocial)
        session.commit()
        session.refresh(redsocial)
        return redsocial
    
    
    @staticmethod
    def eliminar_redsocial(session: Session, redsocial_id: int) -> bool:
        """
        Eliminar una red social por su ID
        """
        redsocial = session.get(Redsocial, redsocial_id)
        if not redsocial:
            return False
        
        session.delete(redsocial)
        session.commit()
        return True
    
    
    @staticmethod
    def contar_redsociales(session: Session) -> int:
        """
        Contar cuántas redes sociales hay registradas
        """
        statement = select(Redsocial)
        redsociales = session.exec(statement).all()
        return len(list(redsociales))
