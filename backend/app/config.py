from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LANGSMITH_TRACING: bool = True
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    MONGODB_URL: str
    ACCESS_TOKEN_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_TIME: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REFRESH_TOKEN_SECRET_KEY: str
    REDIS_URL: str
    SUPABASE_URL: str
    SUPABASE_BUCKET: str
    SUPABASE_SERVICE_ROLE_KEY: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER : str
    MAIL_FROM_EMAIL: str
    MAIL_FROM_NAME: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings()