from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./docgen.db"
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Gemini API
    gemini_api_key: str
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
