from sqlmodel import Session, select
from app.models.modelos import Contenido, Tema, Redsocial
from datetime import datetime, timezone
from typing import List, Optional


class ContenidoController:
    
    @staticmethod
    def crear_contenido(
        session: Session, 
        descripcion: str, 
        tema_id: int, 
        redsocial_id: int,
        archivo_id: int,
        publicado: bool = True,
        fecha_publicacion: Optional[datetime] = None,
        enlace_publicacion: Optional[str] = None
    ) -> Contenido:
        """
        Crear un nuevo contenido
        """
        # Verificar que el tema existe
        tema = session.get(Tema, tema_id)
        if not tema:
            raise ValueError(f"Tema con id {tema_id} no existe")
        
        # Verificar que la red social existe
        redsocial = session.get(Redsocial, redsocial_id)
        if not redsocial:
            raise ValueError(f"Red social con id {redsocial_id} no existe")
        
        # Verificar que el archivo existe
        from app.models.modelos import Archivo
        archivo = session.get(Archivo, archivo_id)
        if not archivo:
            raise ValueError(f"Archivo con id {archivo_id} no existe")
        
        nuevo_contenido = Contenido(
            descripcion=descripcion,
            publicado=publicado,
            fecha_publicacion=fecha_publicacion,
            enlace_publicacion=enlace_publicacion,
            tema_id=tema_id,
            redsocial_id=redsocial_id,
            archivo_id=archivo_id
        )
        session.add(nuevo_contenido)
        session.commit()
        session.refresh(nuevo_contenido)
        return nuevo_contenido
    
    
    @staticmethod
    def obtener_contenido_por_id(session: Session, contenido_id: int) -> Optional[Contenido]:
        """
        Obtener un contenido por su ID
        """
        contenido = session.get(Contenido, contenido_id)
        return contenido
    
    
    @staticmethod
    def obtener_todos_contenidos(session: Session) -> List[Contenido]:
        """
        Obtener todos los contenidos
        """
        statement = select(Contenido)
        contenidos = session.exec(statement).all()
        return list(contenidos)
    
    
    @staticmethod
    def obtener_contenidos_por_tema(session: Session, tema_id: int) -> List[Contenido]:
        """
        Obtener todos los contenidos de un tema específico
        """
        statement = select(Contenido).where(Contenido.tema_id == tema_id)
        contenidos = session.exec(statement).all()
        return list(contenidos)
    
    
    @staticmethod
    def obtener_contenidos_por_redsocial(session: Session, redsocial_id: int) -> List[Contenido]:
        """
        Obtener todos los contenidos de una red social específica
        """
        statement = select(Contenido).where(Contenido.redsocial_id == redsocial_id)
        contenidos = session.exec(statement).all()
        return list(contenidos)
    
    
    @staticmethod
    def obtener_contenidos_publicados(session: Session, publicado: bool = True) -> List[Contenido]:
        """
        Obtener contenidos filtrados por estado de publicación
        """
        statement = select(Contenido).where(Contenido.publicado == publicado)
        contenidos = session.exec(statement).all()
        return list(contenidos)
    
    
    @staticmethod
    def actualizar_contenido(
        session: Session, 
        contenido_id: int, 
        descripcion: Optional[str] = None,
        publicado: Optional[bool] = None,
        fecha_publicacion: Optional[datetime] = None,
        enlace_publicacion: Optional[str] = None,
        tema_id: Optional[int] = None,
        redsocial_id: Optional[int] = None,
        archivo_id: Optional[int] = None
    ) -> Optional[Contenido]:
        """
        Actualizar un contenido existente
        """
        contenido = session.get(Contenido, contenido_id)
        if not contenido:
            return None
        
        # Actualizar campos si se proporcionan
        if descripcion is not None:
            contenido.descripcion = descripcion
        
        if publicado is not None:
            contenido.publicado = publicado
        
        if fecha_publicacion is not None:
            contenido.fecha_publicacion = fecha_publicacion
        
        if enlace_publicacion is not None:
            contenido.enlace_publicacion = enlace_publicacion
        
        if tema_id is not None:
            # Verificar que el nuevo tema existe
            tema = session.get(Tema, tema_id)
            if not tema:
                raise ValueError(f"Tema con id {tema_id} no existe")
            contenido.tema_id = tema_id
        
        if redsocial_id is not None:
            # Verificar que la nueva red social existe
            redsocial = session.get(Redsocial, redsocial_id)
            if not redsocial:
                raise ValueError(f"Red social con id {redsocial_id} no existe")
            contenido.redsocial_id = redsocial_id
        
        if archivo_id is not None:
            # Verificar que el nuevo archivo existe
            from app.models.modelos import Archivo
            archivo = session.get(Archivo, archivo_id)
            if not archivo:
                raise ValueError(f"Archivo con id {archivo_id} no existe")
            contenido.archivo_id = archivo_id
        
        # Actualizar fecha de modificación
        contenido.update_at = datetime.now(timezone.utc)
        
        session.add(contenido)
        session.commit()
        session.refresh(contenido)
        return contenido
    
    
    @staticmethod
    def eliminar_contenido(session: Session, contenido_id: int) -> bool:
        """
        Eliminar un contenido por su ID
        """
        contenido = session.get(Contenido, contenido_id)
        if not contenido:
            return False
        
        session.delete(contenido)
        session.commit()
        return True
    
    
    @staticmethod
    def contar_contenidos_por_tema(session: Session, tema_id: int) -> int:
        """
        Contar cuántos contenidos tiene un tema
        """
        statement = select(Contenido).where(Contenido.tema_id == tema_id)
        contenidos = session.exec(statement).all()
        return len(list(contenidos))
    
    
    @staticmethod
    def contar_contenidos_por_redsocial(session: Session, redsocial_id: int) -> int:
        """
        Contar cuántos contenidos tiene una red social
        """
        statement = select(Contenido).where(Contenido.redsocial_id == redsocial_id)
        contenidos = session.exec(statement).all()
        return len(list(contenidos))
