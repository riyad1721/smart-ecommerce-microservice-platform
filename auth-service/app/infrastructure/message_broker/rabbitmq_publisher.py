import json
import logging
from datetime import datetime
from uuid import UUID

import aio_pika

from app.core.config import settings

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    async def publish_user_registered(
        self,
        user_id: UUID,
        email: str,
        full_name: str
    ) -> None:
        try:
            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

            async with connection:
                channel = await connection.channel()

                exchange = await channel.declare_exchange(
                    settings.RABBITMQ_EXCHANGE,
                    aio_pika.ExchangeType.TOPIC,
                    durable=True
                )

                message_body = {
                    "event_type": "user.registered",
                    "user_id": str(user_id),
                    "email": email,
                    "full_name": full_name,
                    "occurred_at": datetime.utcnow().isoformat()
                }

                message = aio_pika.Message(
                    body=json.dumps(message_body).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                )

                await exchange.publish(
                    message,
                    routing_key="user.registered"
                )

        except Exception as error:
            logger.warning("RabbitMQ publish failed: %s", error)