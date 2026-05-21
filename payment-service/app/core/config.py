from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "payment-service"
    APP_ENV: str = "development"
    APP_PORT: int = 8004

    DATABASE_URL: str = "postgresql://auth_user:auth_pass@127.0.0.1:5433/auth_db"

    JWT_SECRET_KEY: str = "my-secret-key"
    JWT_ALGORITHM: str = "HS256"

    RABBITMQ_URL: str = "amqp://guest:guest@127.0.0.1:5672/"
    RABBITMQ_EXCHANGE: str = "ecommerce_events"

    ORDER_CREATED_QUEUE: str = "payment_order_created_queue"
    ORDER_CREATED_ROUTING_KEY: str = "order.created"

    PAYMENT_COMPLETED_ROUTING_KEY: str = "payment.completed"
    PAYMENT_FAILED_ROUTING_KEY: str = "payment.failed"

    ENABLE_RABBITMQ_CONSUMER: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
