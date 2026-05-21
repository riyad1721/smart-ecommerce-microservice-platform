import json
import logging
import aio_pika
from app.core.config import settings

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    async def publish(self, routing_key: str, message: dict) -> None:
        try:
            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

            async with connection:
                channel = await connection.channel()

                exchange = await channel.declare_exchange(
                    settings.RABBITMQ_EXCHANGE,
                    aio_pika.ExchangeType.TOPIC,
                    durable=True,
                )

                await exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(message).encode(),
                        content_type="application/json",
                    ),
                    routing_key=routing_key,
                )

        except Exception as exc:
            logger.warning("RabbitMQ publish failed: %s", exc)