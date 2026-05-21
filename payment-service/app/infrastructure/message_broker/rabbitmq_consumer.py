import json
import logging
import aio_pika

from app.core.config import settings
from app.domain.events.order_created_event import OrderCreatedEvent
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.payment_repository import PaymentRepository

logger = logging.getLogger(__name__)


async def handle_order_created(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            payload = json.loads(message.body.decode())
            event = OrderCreatedEvent(**payload)

            db = SessionLocal()
            try:
                repository = PaymentRepository(db)

                payment = repository.create_payment(
                    order_id=event.order_id,
                    user_id=event.user_id,
                    amount=event.amount,
                    currency=event.currency,
                )

                logger.info(
                    "Payment record created from order.created event. payment_id=%s order_id=%s",
                    payment.id,
                    payment.order_id,
                )

            finally:
                db.close()

        except Exception as exc:
            logger.exception("Failed to handle order.created event: %s", exc)


async def start_rabbitmq_consumer():
    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            settings.RABBITMQ_EXCHANGE,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = await channel.declare_queue(
            settings.ORDER_CREATED_QUEUE,
            durable=True,
        )

        await queue.bind(
            exchange,
            routing_key=settings.ORDER_CREATED_ROUTING_KEY,
        )

        await queue.consume(handle_order_created)

        logger.info("RabbitMQ consumer started for order.created")

    except Exception as exc:
        logger.error("RabbitMQ consumer not started. Reason: %s", exc)