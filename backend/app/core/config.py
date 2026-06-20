"""
Application configuration settings.
"""
from pydantic import BaseSettings
import secrets
from typing import List, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "CareerHunter AI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Database - Using SQLite for simplicity
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./careerhunter.db"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Google Gemini API
    GEMINI_API_KEY: str = ""

    # JWT
    ALGORITHM: str = "HS256"

    # Email (AWS SES)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    SES_FROM_EMAIL: str = "noreply@careerhunter.ai"

    # File upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    UPLOAD_FOLDER: str = "uploads"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()