from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "auth-service"
    APP_ENV: str = "development"
    APP_PORT: int = 8000

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_EXCHANGE: str = "ecommerce.events"

    class Config:
        env_file = ".env"


settings = Settings()
