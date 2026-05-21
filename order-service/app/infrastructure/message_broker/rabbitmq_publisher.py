import json
import logging
from decimal import Decimal
from uuid import UUID

import aio_pika

from app.core.config import settings

logger = logging.getLogger(__name__)


class EventJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


class RabbitMQPublisher:
    async def publish(self, routing_key: str, payload: dict) -> None:
        try:
            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            async with connection:
                channel = await connection.channel()
                exchange = await channel.declare_exchange(
                    settings.RABBITMQ_EXCHANGE,
                    aio_pika.ExchangeType.TOPIC,
                    durable=True,
                )
                message = aio_pika.Message(
                    body=json.dumps(payload, cls=EventJSONEncoder).encode(),
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                )
                await exchange.publish(message, routing_key=routing_key)
        except Exception as exc:
            logger.warning("RabbitMQ publish failed. API request will continue. Error: %s", exc)
