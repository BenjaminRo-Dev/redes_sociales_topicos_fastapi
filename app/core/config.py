from re import L
from tkinter import W
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
    
    FACEBOOK_TOKEN = os.getenv("FACEBOOK_TOKEN")
    FACEBOOK_ID_PAGINA = os.getenv("FACEBOOK_ID_PAGINA")
    FACEBOOK_API_URL = os.getenv("FACEBOOK_API_URL")
    
    INSTAGRAM_API_URL = os.getenv("INSTAGRAM_API_URL")
    INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")
    INSTAGRAM_ID_CUENTA = os.getenv("INSTAGRAM_ID_CUENTA")
    
    TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
    TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
    TIKTOK_REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI")
    
    TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")
    TIKTOK_OPEN_ID = os.getenv("TIKTOK_OPEN_ID")
    
    TIKTOK_AUTH_URL = os.getenv("TIKTOK_AUTH_URL")
    TIKTOK_TOKEN_URL = os.getenv("TIKTOK_TOKEN_URL")
    
    WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
    WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
    
    LINKEDIN_API_URL = os.getenv("LINKEDIN_API_URL")
    LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
    LINKEDIN_SUBSCRIBER = os.getenv("LINKEDIN_SUBSCRIBER")
    
settings = Settings()

if not settings.DATABASE_URL:
    raise RuntimeError("variable de entorno 'DATABASE_URL' es requerida.")

if not settings.GEMINI_API_KEY:
    raise RuntimeError("variable de entorno 'GEMINI_API_KEY' es requerida.")