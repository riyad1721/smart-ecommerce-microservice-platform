import asyncio
import json
import sys
import uuid

import aio_pika


RABBITMQ_URL = "amqp://guest:guest@127.0.0.1:5672/"
EXCHANGE_NAME = "ecommerce.events"


def build_event(event_type: str) -> tuple[str, dict]:
    event_id = str(uuid.uuid4())

    if event_type == "order.created":
        return event_type, {
            "event_id": event_id,
            "user_id": "user-1",
            "order_id": "order-1001",
            "email": "user1@example.com",
            "total_amount": 1500.50,
        }

    if event_type == "payment.completed":
        return event_type, {
            "event_id": event_id,
            "user_id": "user-1",
            "order_id": "order-1001",
            "payment_id": "pay-1001",
            "email": "user1@example.com",
            "amount": 1500.50,
        }

    if event_type == "payment.failed":
        return event_type, {
            "event_id": event_id,
            "user_id": "user-1",
            "order_id": "order-1002",
            "payment_id": "pay-1002",
            "email": "user1@example.com",
            "reason": "Insufficient balance",
        }

    raise ValueError("Invalid event type")


async def main() -> None:
    event_type = sys.argv[1] if len(sys.argv) > 1 else "order.created"
    routing_key, payload = build_event(event_type)

    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            EXCHANGE_NAME,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        message = aio_pika.Message(
            body=json.dumps(payload).encode("utf-8"),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await exchange.publish(message, routing_key=routing_key)

        print(f"Published event: {routing_key}")
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
