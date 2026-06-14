from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    LANGSMITH_TRACING: bool = True
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    MONGODB_URL: str
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_TIME: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REFRESH_TOKEN_SECRET_KEY: str
    REDIS_URL: str
    SUPABASE_URL: str
    SUPABASE_BUCKET: str
    SUPABASE_PUBLISHABLE_KEY: str # This is your Public / Publishable API Key
    SUPABASE_SECRET_KEY: str # This is your Secret API Key
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER : str
    MAIL_FROM_NAME: str
    MAIL_FROM: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    FRONTEND_DOMAIN: str
    ENV: str

    model_config = SettingsConfigDict(env_file=(".env", "../.env", "app/.env"), extra="ignore")

Config = Settings()