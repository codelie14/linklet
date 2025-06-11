import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Bot Configuration
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    telegram_webhook_url: Optional[str] = Field(None, env="TELEGRAM_WEBHOOK_URL")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # AI Services
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    
    # n8n Integration
    n8n_base_url: Optional[str] = Field(None, env="N8N_BASE_URL")
    n8n_api_key: Optional[str] = Field(None, env="N8N_API_KEY")
    
    # Security
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    
    # Performance
    rate_limit_requests: int = Field(default=30, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    class Config:
        env_file = ".env"

settings = Settings()