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
    
    
    @staticmethod
    def obtener_historial_tema(session: Session, tema_id: int) -> Optional[dict]:
        """
        Obtiene todos los prompts y contenidos de un tema ordenados por fecha de creación.
        Retorna una lista combinada ordenada cronológicamente para simular un chat.
        """
        from app.models.modelos import Prompt, Contenido, Archivo, Redsocial
        
        tema = session.get(Tema, tema_id)
        if not tema:
            return None
        
        # Obtener todos los prompts del tema
        statement_prompts = select(Prompt).where(Prompt.tema_id == tema_id)
        prompts = session.exec(statement_prompts).all()
        
        # Obtener todos los contenidos del tema con sus relaciones
        statement_contenidos = select(Contenido).where(Contenido.tema_id == tema_id)
        contenidos = session.exec(statement_contenidos).all()
        
        # Crear lista unificada con información formateada
        historial = []
        
        # Agregar prompts
        for prompt in prompts:
            historial.append({
                "tipo": "prompt",
                "id": prompt.id,
                "descripcion": prompt.descripcion,
                "tema_id": prompt.tema_id,
                "create_at": prompt.create_at,
                "update_at": prompt.update_at
            })
        
        # Agregar contenidos con sus relaciones
        for contenido in contenidos:
            # Obtener archivo relacionado
            archivo = session.get(Archivo, contenido.archivo_id)
            # Obtener red social relacionada
            redsocial = session.get(Redsocial, contenido.redsocial_id)
            
            historial.append({
                "tipo": "contenido",
                "id": contenido.id,
                "descripcion": contenido.descripcion,
                "publicado": contenido.publicado,
                "fecha_publicacion": contenido.fecha_publicacion,
                "enlace_publicacion": contenido.enlace_publicacion,
                "tema_id": contenido.tema_id,
                "redsocial_id": contenido.redsocial_id,
                "redsocial_nombre": redsocial.nombre if redsocial else None,
                "archivo_id": contenido.archivo_id,
                "archivo_url": archivo.url if archivo else None,
                "archivo_prompt_text": archivo.prompt_text if archivo else None,
                "create_at": contenido.create_at,
                "update_at": contenido.update_at
            })
        
        # Ordenar toda la lista por fecha de creación (más antiguo primero)
        historial.sort(key=lambda x: x["create_at"])
        
        return {
            "tema_id": tema.id,
            "tema_nombre": tema.nombre,
            "usuario_id": tema.usuario_id,
            "historial": historial
        }
