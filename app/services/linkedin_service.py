import requests
import os
from urllib.parse import urlparse
from app.core.config import settings


class LinkedInService:
    def __init__(self):
        self.token = settings.LINKEDIN_TOKEN
        self.subscriber = settings.LINKEDIN_SUBSCRIBER
        self.api_url = settings.LINKEDIN_API_URL
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    
    def __registrar_subida_imagen(self):
        """Paso 1. se obtiene el uploadUrl y asset"""
        url = f"{self.api_url}/assets?action=registerUpload"
        
        body = {
            "registerUploadRequest": {
                "recipes": [
                    "urn:li:digitalmediaRecipe:feedshare-image"
                ],
                "owner": f"urn:li:person:{self.subscriber}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        
        respuesta = requests.post(url, json=body, headers=self.headers)
        respuesta.raise_for_status()
        
        data = respuesta.json()
        upload_url = data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset = data["value"]["asset"]
        
        return {
            "upload_url": upload_url,
            "asset": asset
        }
    
    
    def __subir_imagen(self, upload_url: str, url_img: str):
        """ Paso 2: Subir el archivo binario de la imagen a LinkedIn """
        obtener_imagen = requests.get(url_img)
        obtener_imagen.raise_for_status()
        binarios_imagen = obtener_imagen.content
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        respuesta = requests.post(upload_url, data=binarios_imagen, headers=headers)
        respuesta.raise_for_status()
        
        return respuesta.status_code == 201
    
    
    def __crear_publicacion(self, asset: str, texto: str):
        """ Paso 3: Crear la publicacion con la imagen """
        
        url = f"{self.api_url}/ugcPosts"
        
        body = {
            "author": f"urn:li:person:{self.subscriber}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": texto
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset,
                            "title": {
                                "text": "Publicación"
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        respuesta = requests.post(url, json=body, headers=self.headers)
        respuesta.raise_for_status()
        
        return respuesta.json() #retorna: {'id': 'urn:li:share:7399650761497833474'}
    
    
    def publicar(self, texto: str, url_img: str):
        try:
            registro = self.__registrar_subida_imagen()
            upload_url = registro["upload_url"]
            asset = registro["asset"]
            
            self.__subir_imagen(upload_url, url_img)
            
            respuesta = self.__crear_publicacion(asset, texto)
            respuesta["enlace"] = f"https://www.linkedin.com/feed/update/{respuesta['id']}"
            
            return respuesta
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Error al publicar en LinkedIn: {str(e)}"
            }
        except FileNotFoundError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error inesperado: {str(e)}"
            }


linkedin_service = LinkedInService()
