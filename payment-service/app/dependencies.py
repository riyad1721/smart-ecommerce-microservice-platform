from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.payment_repository import PaymentRepository
from app.infrastructure.message_broker.rabbitmq_publisher import RabbitMQPublisher
from app.application.services.payment_service import PaymentService


def get_payment_repository(
    db: Session = Depends(get_db),
) -> PaymentRepository:
    return PaymentRepository(db)


def get_rabbitmq_publisher() -> RabbitMQPublisher:
    return RabbitMQPublisher()


def get_payment_service(
    repository: PaymentRepository = Depends(get_payment_repository),
    publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
) -> PaymentService:
    return PaymentService(repository, publisher)