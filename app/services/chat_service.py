import json
from textwrap import dedent
from fastapi.responses import JSONResponse
from app.schemas.chat_schema import ChatRequest
from app.services import ia_service


def _construir_instrucciones(redes_sociales: list[str]) -> str:
    redes_formateadas = ", ".join(redes_sociales)

    instrucciones = dedent(f"""
        Sos un asistente especializado en generar contenido académico para redes sociales de la administración de la 'Facultad de Computación - FICCT' de la UAGRM en Santa Cruz, Bolivia.

        REGLAS IMPORTANTES:
        - Respondé ÚNICAMENTE con formato JSON válido
        - No incluyás texto adicional antes o después del JSON
        - No uses markdown ni bloques de código
        - Adaptá el tono y contenido según cada red social (por ejemplo: formal, amigable, etc.)
        - Longitud predeterminada: corta (a menos que se especifique otra)
        - Utiliza el uso pronominal y verbal de "vos" en lugar de "tú"

        REDES SOCIALES A CONSIDERAR:
        {redes_formateadas}

        ESTRUCTURA DE LA RESPUESTA (JSON):
        {{
        "tema": "Breve descripcion del tema (max 5 palabras)"
        "red_social_1": {{
            "texto": "Contenido adaptado para Facebook",
            "hashtags": ["#hashtag1", "#hashtag2"]
        }},
        "red_social_n": {{
            "texto": "Contenido adaptado para Instagram",
            "hashtags": ["#hashtag1", "#hashtag2"]
        }}
        }}

        Genera contenido apropiado para cada red social especificada.
        """
    ).strip()
    
    return instrucciones


def generar_contenido(solicitud: ChatRequest) -> JSONResponse:
    return __generar_contenido(solicitud, 3)


def __generar_contenido(solicitud: ChatRequest, intentos: int) -> JSONResponse:

    instrucciones: str = _construir_instrucciones(solicitud.redes_sociales)
    contenido_ia: str = ia_service.generar_contenido(solicitud.prompt, instrucciones)

    try:
        return JSONResponse(status_code=200, content=json.loads(contenido_ia))
    except Exception as e:
        print(
            f"Error al convertir el texto generado por la IA a JSON - Intentos restantes: {intentos-1}",
            e,
        )

        if intentos > 0:
            return __generar_contenido(solicitud, intentos - 1)

    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "mensaje": "La IA No generó el formato correcto en JSON",
        },
    )
