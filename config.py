"""
Configuration settings for Chuco AI application
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application settings
    APP_NAME: str = "Chuco AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database settings
    DATABASE_URL: str = "sqlite:///./chucoai.db"  # Default to SQLite for development
    # For production PostgreSQL: "postgresql://user:password@localhost/chucoai"

    # Email settings (using SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "yo@chuco.ai"
    SMTP_FROM_NAME: str = "Chuco AI"

    # Notification settings
    ADMIN_EMAIL: str = "yo@chuco.ai"
    ADMIN_NAME: str = "David Negrete"
    SEND_EMAIL_NOTIFICATIONS: bool = True

    # Security settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALLOWED_ORIGINS: list = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://chuco.ai",
        "https://www.chuco.ai",
    ]

    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 10  # Max form submissions per minute per IP

    # Captcha settings (optional)
    RECAPTCHA_ENABLED: bool = False
    RECAPTCHA_SITE_KEY: str = ""
    RECAPTCHA_SECRET_KEY: str = ""

    # Business settings
    BUSINESS_PHONE: str = "(844) 915-2828"
    BUSINESS_EMAIL: str = "yo@chuco.ai"
    BUSINESS_LOCATION: str = "El Paso, Texas"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


def get_settings():
    """Dependency to get settings"""
    return settings
