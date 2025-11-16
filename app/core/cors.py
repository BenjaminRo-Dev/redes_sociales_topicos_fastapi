from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def configuracion_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.APP_VUEJS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
