"""
Configuration settings for the Payments API application.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "Payments API"
    api_version: str = "v2.0.8"

settings = Settings()
