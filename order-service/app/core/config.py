from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "order-service"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg2://auth_user:auth_pass@127.0.0.1:5433/auth_db"

    JWT_SECRET_KEY: str = "my-secret-key"
    JWT_ALGORITHM: str = "HS256"

    PRODUCT_SERVICE_BASE_URL: str = "http://127.0.0.1:8001"

    RABBITMQ_URL: str = "amqp://guest:guest@127.0.0.1:5672/"
    RABBITMQ_EXCHANGE: str = "ecommerce.events"
    ORDER_CREATED_ROUTING_KEY: str = "order.created"
    PAYMENT_COMPLETED_ROUTING_KEY: str = "payment.completed"
    PAYMENT_FAILED_ROUTING_KEY: str = "payment.failed"

    ENABLE_RABBITMQ_CONSUMER: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
