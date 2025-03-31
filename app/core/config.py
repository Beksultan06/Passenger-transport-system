# Новый импорт
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Passenger Transport System"
    DATABASE_URL: str = "postgresql://fast:fast@localhost/fast"
    JWT_SECRET: str = "supersecret"
    REDIS_URL: str = "redis://localhost:6379/0"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()