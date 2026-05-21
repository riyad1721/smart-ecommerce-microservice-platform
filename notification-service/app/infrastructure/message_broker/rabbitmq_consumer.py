import asyncio
import json
import logging
from typing import Any

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from app.application.services.notification_service import NotificationService
from app.application.use_cases.send_order_notification import SendOrderNotificationUseCase
from app.application.use_cases.send_payment_notification import (
    SendPaymentCompletedNotificationUseCase,
    SendPaymentFailedNotificationUseCase,
)
from app.core.config import settings
from app.domain.events.order_created_event import OrderCreatedEvent
from app.domain.events.payment_completed_event import PaymentCompletedEvent
from app.domain.events.payment_failed_event import PaymentFailedEvent
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.notification_repository import NotificationRepository

logger = logging.getLogger(__name__)

ROUTING_KEYS = [
    "order.created",
    "payment.completed",
    "payment.failed",
]


def _extract_payload(raw_message: dict[str, Any]) -> dict[str, Any]:
    if "data" in raw_message and isinstance(raw_message["data"], dict):
        payload = raw_message["data"]

        if "event_id" not in payload and raw_message.get("event_id"):
            payload["event_id"] = raw_message.get("event_id")

        return payload

    return raw_message


async def start_rabbitmq_consumer() -> None:
    if not settings.RABBITMQ_ENABLED:
        logger.info("RabbitMQ consumer disabled by configuration")
        return

    while True:
        try:
            logger.info("Connecting to RabbitMQ: %s", settings.RABBITMQ_URL)

            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=10)

            exchange = await channel.declare_exchange(
                settings.RABBITMQ_EXCHANGE,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )

            queue = await channel.declare_queue(
                settings.RABBITMQ_QUEUE,
                durable=True,
            )

            for routing_key in ROUTING_KEYS:
                await queue.bind(exchange, routing_key=routing_key)

            logger.info("RabbitMQ consumer started successfully")

            await queue.consume(process_message)

            await asyncio.Future()

        except Exception as exc:
            logger.error(
                "RabbitMQ unavailable or consumer crashed: %s. Retrying in 10 seconds.",
                exc,
            )
            await asyncio.sleep(10)


async def process_message(message: AbstractIncomingMessage) -> None:
    async with message.process(requeue=False):
        routing_key = message.routing_key

        try:
            raw_message = json.loads(message.body.decode("utf-8"))
            payload = _extract_payload(raw_message)

            logger.info("Received event. routing_key=%s payload=%s", routing_key, payload)

            db = SessionLocal()

            try:
                repository = NotificationRepository(db)
                service = NotificationService(repository)

                if routing_key == "order.created":
                    event = OrderCreatedEvent(**payload)
                    SendOrderNotificationUseCase(service).execute(event)

                elif routing_key == "payment.completed":
                    event = PaymentCompletedEvent(**payload)
                    SendPaymentCompletedNotificationUseCase(service).execute(event)

                elif routing_key == "payment.failed":
                    event = PaymentFailedEvent(**payload)
                    SendPaymentFailedNotificationUseCase(service).execute(event)

                else:
                    logger.warning("Unknown routing key ignored: %s", routing_key)

            finally:
                db.close()

        except Exception:
            logger.exception("Failed to process RabbitMQ message")
