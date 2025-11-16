from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    
    APP_VUEJS = os.getenv("APP_VUEJS")
    
settings = Settings()

if not settings.DATABASE_URL:
    raise RuntimeError("variable de entorno 'DATABASE_URL' es requerida.")

if not settings.GEMINI_API_KEY:
    raise RuntimeError("variable de entorno 'GEMINI_API_KEY' es requerida.")