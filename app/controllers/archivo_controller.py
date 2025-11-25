from sqlmodel import Session, select
from app.models.modelos import Archivo, Contenido
from datetime import datetime, timezone
from typing import List, Optional


class ArchivoController:
    
    @staticmethod
    def crear_archivo(session: Session, url: str, prompt_text: Optional[str] = None) -> Archivo:
        """
        Crear un nuevo archivo
        """
        nuevo_archivo = Archivo(
            url=url,
            prompt_text=prompt_text
        )
        session.add(nuevo_archivo)
        session.commit()
        session.refresh(nuevo_archivo)
        return nuevo_archivo
    
    
    @staticmethod
    def obtener_archivo_por_id(session: Session, archivo_id: int) -> Optional[Archivo]:
        """
        Obtener un archivo por su ID
        """
        archivo = session.get(Archivo, archivo_id)
        return archivo
    
    
    @staticmethod
    def obtener_todos_archivos(session: Session) -> List[Archivo]:
        """
        Obtener todos los archivos
        """
        statement = select(Archivo)
        archivos = session.exec(statement).all()
        return list(archivos)
    
    
    @staticmethod
    def obtener_archivos_por_contenido(session: Session, contenido_id: int) -> Optional[Archivo]:
        """
        Obtener el archivo de un contenido específico
        """
        contenido = session.get(Contenido, contenido_id)
        if not contenido:
            return None
        
        archivo = session.get(Archivo, contenido.archivo_id)
        return archivo
    
    
    @staticmethod
    def actualizar_archivo(
        session: Session, 
        archivo_id: int, 
        url: Optional[str] = None,
        prompt_text: Optional[str] = None
    ) -> Optional[Archivo]:
        """
        Actualizar un archivo existente
        """
        archivo = session.get(Archivo, archivo_id)
        if not archivo:
            return None
        
        # Actualizar campos si se proporcionan
        if url is not None:
            archivo.url = url
        
        if prompt_text is not None:
            archivo.prompt_text = prompt_text
        
        # Actualizar fecha de modificación
        archivo.update_at = datetime.now(timezone.utc)
        
        session.add(archivo)
        session.commit()
        session.refresh(archivo)
        return archivo
    
    
    @staticmethod
    def eliminar_archivo(session: Session, archivo_id: int) -> bool:
        """
        Eliminar un archivo por su ID
        """
        archivo = session.get(Archivo, archivo_id)
        if not archivo:
            return False
        
        session.delete(archivo)
        session.commit()
        return True
    
    
    @staticmethod
    def contar_archivos_sin_contenido(session: Session) -> int:
        """
        Contar cuántos archivos hay en total
        """
        statement = select(Archivo)
        archivos = session.exec(statement).all()
        return len(list(archivos))
