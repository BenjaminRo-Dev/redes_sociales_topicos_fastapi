import httpx
from fastapi import UploadFile, HTTPException
from typing import Dict, Tuple

from app.core.config import Settings

settings = Settings()


class TiktokPostService:

    def __init__(self):
        self.access_token: str | None = settings.TIKTOK_ACCESS_TOKEN
        self.init_url: str = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        self.status_url: str = (
            "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
        )

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        }

    async def _inicializar_subida(self, texto: str, video_size: int) -> Tuple[str, str]:
        headers = self._headers()

        cuerpo = {
            "post_info": {
                "title": texto,
                "privacy_level": "SELF_ONLY",
                "disable_duet": False,
                "disable_comment": True,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": video_size,
                "total_chunk_count": 1,
            },
        }

        async with httpx.AsyncClient(timeout=60) as client:
            respuesta = await client.post(self.init_url, headers=headers, json=cuerpo)

        if respuesta.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Falló la inicialización de la subida: {respuesta.text}",
            )

        data = respuesta.json()["data"]
        return data["publish_id"], data["upload_url"]

    async def _subir_video(self, upload_url: str, archivo: UploadFile, video_size: int) -> bool:
        """Sube el video al bucket de TikTok."""
        headers = {
            "Content-Type": "video/mp4",
            "Content-Range": f"bytes 0-{video_size-1}/{video_size}",
        }

        async with httpx.AsyncClient(timeout=120) as client:
            respuesta = await client.put(
                upload_url, headers=headers, content=await archivo.read()
            )

        if respuesta.status_code not in (200, 201):
            raise HTTPException(
                status_code=500, detail=f"Falló la subida del video: {respuesta.text}"
            )

        return True


    async def _obtener_estado_publicacion(self, publish_id: str) -> Dict:
        """Consulta el estado de una publicación en TikTok."""
        headers = self._headers()
        cuerpo = {"publish_id": publish_id}

        async with httpx.AsyncClient(timeout=30) as client:
            respuesta = await client.post(self.status_url, headers=headers, json=cuerpo)

        if respuesta.status_code != 200:
            return {"status": "error_check", "details": respuesta.text}

        return respuesta.json()


    async def publicar_video(self, texto: str, archivo: UploadFile) -> Dict[str, str | Dict]:
        """Publica un video en TikTok."""
        contenido = await archivo.read()
        video_size = len(contenido)
        await archivo.seek(0)

        # Inicializar la subida
        publish_id, upload_url = await self._inicializar_subida(texto, video_size)

        # Subir el video
        await self._subir_video(upload_url, archivo, video_size)

        # Obtener el estado de la publicación
        estado_publicacion = await self._obtener_estado_publicacion(publish_id)

        return {
            "estado": "Subido",
            "mensaje": "El video se subió y TikTok lo está procesando.",
            "publish_id": publish_id,
            "estado_publicacion": estado_publicacion,
        }
