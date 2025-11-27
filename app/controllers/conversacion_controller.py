from sqlmodel import Session, select, desc, asc
from app.models.modelos import Conversacion, Mensaje, Usuario
from datetime import datetime, timezone
from typing import List, Optional
from app.services.chat_service import generar_contenido
from app.schemas.chat_schema import ChatRequest


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
    
    
    @staticmethod
    def agregar_mensaje_con_ia(
        session: Session,
        conversacion_id: int,
        prompt_usuario: str,
        redes_sociales: List[str],
        duracion_video: int = 4
    ) -> List[Mensaje]:
        """
        Procesa la solicitud del usuario, genera contenido con IA para múltiples redes sociales
        y guarda cada respuesta como un mensaje individual en la base de datos.
        """
        # Verificar que la conversación existe
        conversacion = session.get(Conversacion, conversacion_id)
        if not conversacion:
            raise ValueError(f"Conversación con id {conversacion_id} no existe")
        
        # Guardar el mensaje del usuario
        mensaje_usuario = Mensaje(
            emisor="usuario",
            texto=prompt_usuario,
            red_social=None,
            url_archivo=None,
            publicado=False,
            url_publicacion=None,
            conversacion_id=conversacion_id
        )
        session.add(mensaje_usuario)
        
        # Llamar al servicio de generación de contenido
        chat_request = ChatRequest(
            prompt=prompt_usuario,
            duracion_video=duracion_video,
            redes_sociales=redes_sociales
        )
        
        respuesta_ia = generar_contenido(chat_request)
        import json
        # La respuesta es un JSONResponse, extraer el contenido
        contenido_json = json.loads(respuesta_ia.body)
        
        # Extraer los prompts de imagen y video
        prompt_imagen = contenido_json.get("prompt_imagen", None)
        prompt_video = contenido_json.get("prompt_video", None)
        
        # Lista para almacenar los mensajes generados
        mensajes_generados = [mensaje_usuario]
        
        # Mapeo de redes sociales en el JSON de respuesta
        redes_disponibles = ["facebook", "instagram", "linkedin", "whatsapp", "tiktok"]
        
        # Crear un mensaje por cada red social que tenga contenido
        for red in redes_disponibles:
            if red in contenido_json and contenido_json[red]:
                red_data = contenido_json[red]
                
                # Concatenar texto con hashtags
                texto_completo = red_data.get("texto", "")
                hashtags = red_data.get("hashtags", [])
                
                if hashtags:
                    texto_completo += "\n\n" + " ".join(hashtags)
                
                mensaje_ia = Mensaje(
                    emisor="ia",
                    texto=texto_completo,
                    red_social=red,
                    url_archivo=None,  # Se puede actualizar después con url_imagen o url_video
                    publicado=False,
                    url_publicacion=None,
                    prompt_imagen=prompt_imagen,
                    prompt_video=prompt_video,
                    conversacion_id=conversacion_id
                )
                session.add(mensaje_ia)
                mensajes_generados.append(mensaje_ia)
        
        # Actualizar fecha de modificación de la conversación
        conversacion.update_at = datetime.now(timezone.utc)
        session.add(conversacion)
        
        # Commit y refresh de todos los mensajes
        session.commit()
        for mensaje in mensajes_generados:
            session.refresh(mensaje)
        
        return mensajes_generados
