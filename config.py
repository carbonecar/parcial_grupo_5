"""
Configuration settings for the Payments API application.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "Payments API"
    api_version: str = "v1.1.1"

settings = Settings()
