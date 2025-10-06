import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Anonymous Social Platform"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/anon_db")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_long_and_random")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Image Upload Settings
    IMAGE_UPLOAD_DIR: str = "app/static/images"
    MAX_IMAGE_SIZE_MB: int = 2
    ALLOWED_IMAGE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    IMAGE_MAX_WIDTH: int = 1200
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
