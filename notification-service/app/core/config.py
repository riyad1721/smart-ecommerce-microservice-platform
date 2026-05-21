from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "notification-service"
    APP_ENV: str = "development"
    APP_PORT: int = 8005
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg2://auth_user:auth_pass@127.0.0.1:5433/auth_db"

    RABBITMQ_ENABLED: bool = True
    RABBITMQ_URL: str = "amqp://guest:guest@127.0.0.1:5672/"
    RABBITMQ_EXCHANGE: str = "ecommerce.events"
    RABBITMQ_QUEUE: str = "notification-service-queue"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
