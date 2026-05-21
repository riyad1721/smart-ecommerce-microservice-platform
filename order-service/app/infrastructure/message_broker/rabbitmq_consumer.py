import asyncio
import json
import logging
from uuid import UUID

import aio_pika

from app.core.config import settings
from app.domain.entities.order import OrderStatus
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.order_repository import OrderRepository

logger = logging.getLogger(__name__)


async def _handle_payment_completed(payload: dict) -> None:
    order_id = UUID(payload["order_id"])
    with SessionLocal() as db:
        OrderRepository(db).update_status(order_id, OrderStatus.PAID)


async def _handle_payment_failed(payload: dict) -> None:
    order_id = UUID(payload["order_id"])
    with SessionLocal() as db:
        OrderRepository(db).update_status(order_id, OrderStatus.PAYMENT_FAILED)


async def start_payment_event_consumer() -> None:
    if not settings.ENABLE_RABBITMQ_CONSUMER:
        logger.info("RabbitMQ consumer disabled by configuration.")
        return

    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            settings.RABBITMQ_EXCHANGE,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = await channel.declare_queue("order-service.payment-events", durable=True)
        await queue.bind(exchange, routing_key=settings.PAYMENT_COMPLETED_ROUTING_KEY)
        await queue.bind(exchange, routing_key=settings.PAYMENT_FAILED_ROUTING_KEY)

        async def on_message(message: aio_pika.IncomingMessage) -> None:
            async with message.process(requeue=False):
                payload = json.loads(message.body.decode())
                routing_key = message.routing_key

                if routing_key == settings.PAYMENT_COMPLETED_ROUTING_KEY:
                    await _handle_payment_completed(payload)
                elif routing_key == settings.PAYMENT_FAILED_ROUTING_KEY:
                    await _handle_payment_failed(payload)

        await queue.consume(on_message)
        logger.info("RabbitMQ payment event consumer started.")
        await asyncio.Future()
    except Exception as exc:
        logger.warning("RabbitMQ consumer could not start. API will continue. Error: %s", exc)
