from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
settings = Settings()

if not settings.DATABASE_URL:
    raise RuntimeError("variable de entorno 'DATABASE_URL' es requerida.")

