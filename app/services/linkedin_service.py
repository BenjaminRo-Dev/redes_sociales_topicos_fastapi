import requests
import os
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
        """Paso 1. Obtener el uploadUrl y asset"""
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
    
    
    def __subir_imagen(self, upload_url: str, image_path: str):
        """ Paso 2: Subir el archivo binario de la imagen a LinkedIn """
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"La imagen no existe en la ruta: {image_path}")
        
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        respuesta = requests.post(upload_url, data=image_data, headers=headers)
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
        
        # El ID del post creado viene en el header X-RestLi-Id
        post_id = respuesta.headers.get('X-RestLi-Id', 'unknown')
        
        return {
            "status": "success",
            "post_id": post_id,
            "message": "Publicación creada en LinkedIn =)"
        }
    
    
    def publicar_imagen(self, imagen_ruta: str, texto: str):
        """  Método principal que orquesta todo el proceso de publicación """
        try:
            registro = self.__registrar_subida_imagen()
            upload_url = registro["upload_url"]
            asset = registro["asset"]
            
            self.__subir_imagen(upload_url, imagen_ruta)
            
            respuesta = self.__crear_publicacion(asset, texto)
            
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
