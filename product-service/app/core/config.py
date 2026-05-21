from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "product-service"
    APP_ENV: str = "development"
    APP_PORT: int = 8001

    DATABASE_URL: str = "postgresql://auth_user:auth_pass@127.0.0.1:5433/auth_db"

    JWT_SECRET_KEY: str = "my-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    RABBITMQ_URL: str = "amqp://guest:guest@127.0.0.1:5672/"
    RABBITMQ_EXCHANGE: str = "ecommerce.events"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
