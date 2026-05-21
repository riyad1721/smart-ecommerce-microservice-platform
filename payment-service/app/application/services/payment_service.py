import random

from fastapi import HTTPException, status

from app.domain.entities.payment import PaymentStatus
from app.domain.events.payment_completed_event import PaymentCompletedEvent
from app.domain.events.payment_failed_event import PaymentFailedEvent
from app.infrastructure.repositories.payment_repository import PaymentRepository
from app.infrastructure.message_broker.rabbitmq_publisher import RabbitMQPublisher
from app.core.config import settings


class PaymentService:
    def __init__(
        self,
        repository: PaymentRepository,
        publisher: RabbitMQPublisher,
    ):
        self.repository = repository
        self.publisher = publisher

    async def process_payment(
        self,
        payment_id: str,
        force_result: str | None = None,
    ):
        payment = self.repository.get_by_id(payment_id)

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found",
            )

        if payment.status == PaymentStatus.COMPLETED.value:
            return payment

        self.repository.update_status(payment, PaymentStatus.PROCESSING)

        if force_result:
            is_success = force_result.upper() == "SUCCESS"
        else:
            is_success = random.choice([True, True, False])

        if is_success:
            updated_payment = self.repository.update_status(
                payment,
                PaymentStatus.COMPLETED,
            )

            event = PaymentCompletedEvent(
                payment_id=str(updated_payment.id),
                order_id=updated_payment.order_id,
                user_id=updated_payment.user_id,
                amount=updated_payment.amount,
                currency=updated_payment.currency,
                status=updated_payment.status,
            )

            await self.publisher.publish_event(
                settings.PAYMENT_COMPLETED_ROUTING_KEY,
                event.model_dump(),
            )

            return updated_payment

        updated_payment = self.repository.update_status(
            payment,
            PaymentStatus.FAILED,
            failure_reason="Fake payment gateway rejected transaction",
        )

        event = PaymentFailedEvent(
            payment_id=str(updated_payment.id),
            order_id=updated_payment.order_id,
            user_id=updated_payment.user_id,
            amount=updated_payment.amount,
            currency=updated_payment.currency,
            status=updated_payment.status,
            reason=updated_payment.failure_reason or "Payment failed",
        )

        await self.publisher.publish_event(
            settings.PAYMENT_FAILED_ROUTING_KEY,
            event.model_dump(),
        )

        return updated_payment