from sqlmodel import Session, select, desc, asc
from app.models.modelos import Conversacion, Mensaje, Usuario
from datetime import datetime, timezone
from typing import List, Optional


class ConversacionController:
    
    @staticmethod
    def crear_conversacion(session: Session, titulo: str, usuario_id: int) -> Conversacion:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError(f"Usuario con id {usuario_id} no existe")
        
        nueva_conversacion = Conversacion(
            titulo=titulo,
            usuario_id=usuario_id
        )
        session.add(nueva_conversacion)
        session.commit()
        session.refresh(nueva_conversacion)
        return nueva_conversacion
    
    
    @staticmethod
    def obtener_conversacion_por_id(session: Session, conversacion_id: int) -> Optional[Conversacion]:
        conversacion = session.get(Conversacion, conversacion_id)
        return conversacion
    
    
    @staticmethod
    def obtener_todas_conversaciones(session: Session, usuario_id: int) -> List[Conversacion]:
        statement = select(Conversacion).where(
            Conversacion.usuario_id == usuario_id
        ).order_by(desc(Conversacion.update_at))
        conversaciones = session.exec(statement).all()
        return list(conversaciones)
    
    
    @staticmethod
    def obtener_mensajes_conversacion(session: Session, conversacion_id: int) -> List[Mensaje]:
        conversacion = session.get(Conversacion, conversacion_id)
        if not conversacion:
            raise ValueError(f"Conversación con id {conversacion_id} no existe")
        
        statement = select(Mensaje).where(
            Mensaje.conversacion_id == conversacion_id
        ).order_by(asc(Mensaje.create_at))
        mensajes = session.exec(statement).all()
        return list(mensajes)
    
    
    @staticmethod
    def agregar_mensaje(
        session: Session,
        conversacion_id: int,
        emisor: str,
        texto: str,
        red_social: Optional[str] = None,
        url_archivo: Optional[str] = None,
        publicado: bool = False,
        url_publicacion: Optional[str] = None
    ) -> Mensaje:
        conversacion = session.get(Conversacion, conversacion_id)
        if not conversacion:
            raise ValueError(f"Conversación con id {conversacion_id} no existe")
        
        nuevo_mensaje = Mensaje(
            emisor=emisor,
            texto=texto,
            red_social=red_social,
            url_archivo=url_archivo,
            publicado=publicado,
            url_publicacion=url_publicacion,
            conversacion_id=conversacion_id
        )
        
        # Actualizar fecha de modificación de la conversación
        conversacion.update_at = datetime.now(timezone.utc)
        
        session.add(nuevo_mensaje)
        session.add(conversacion)
        session.commit()
        session.refresh(nuevo_mensaje)
        return nuevo_mensaje
    
    
    @staticmethod
    def actualizar_conversacion(
        session: Session,
        conversacion_id: int,
        titulo: Optional[str] = None
    ) -> Optional[Conversacion]:
        conversacion = session.get(Conversacion, conversacion_id)
        if not conversacion:
            return None
        
        if titulo is not None:
            conversacion.titulo = titulo
        
        conversacion.update_at = datetime.now(timezone.utc)
        
        session.add(conversacion)
        session.commit()
        session.refresh(conversacion)
        return conversacion
    
    
    @staticmethod
    def eliminar_conversacion(session: Session, conversacion_id: int) -> bool:
        conversacion = session.get(Conversacion, conversacion_id)
        if not conversacion:
            return False
        
        session.delete(conversacion)
        session.commit()
        return True
    
    
    @staticmethod
    def contar_conversaciones_por_usuario(session: Session, usuario_id: int) -> int:
        statement = select(Conversacion).where(Conversacion.usuario_id == usuario_id)
        conversaciones = session.exec(statement).all()
        return len(list(conversaciones))
