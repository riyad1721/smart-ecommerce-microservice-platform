import asyncio
from uuid import UUID

from fastapi import HTTPException, status

from app.core.config import settings
from app.domain.entities.order import OrderStatus
from app.domain.events.order_created_event import OrderCreatedEvent
from app.infrastructure.message_broker.rabbitmq_publisher import RabbitMQPublisher
from app.infrastructure.repositories.cart_repository import CartRepository
from app.infrastructure.repositories.order_repository import OrderRepository
from app.schemas.order_schema import OrderResponse, OrderItemResponse


class OrderService:
    def __init__(
        self,
        cart_repository: CartRepository,
        order_repository: OrderRepository,
        publisher: RabbitMQPublisher,
    ):
        self.cart_repository = cart_repository
        self.order_repository = order_repository
        self.publisher = publisher

    async def create_order_from_cart(self, user_id: str) -> OrderResponse:
        cart = self.cart_repository.get_by_user_id(user_id)

        if not cart or not cart.items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

        order = self.order_repository.create_from_cart(user_id, cart.items)
        self.cart_repository.clear_cart(user_id)

        event = OrderCreatedEvent(
            order_id=order.id,
            user_id=order.user_id,
            total_amount=order.total_amount,
        )

        asyncio.create_task(
            self.publisher.publish(
                settings.ORDER_CREATED_ROUTING_KEY,
                event.model_dump(),
            )
        )

        return self._to_response(order)

    def get_order(self, order_id: UUID, user_id: str) -> OrderResponse:
        order = self.order_repository.get_by_id_and_user_id(order_id, user_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return self._to_response(order)

    def list_user_orders(self, user_id: str) -> list[OrderResponse]:
        return [self._to_response(order) for order in self.order_repository.list_by_user_id(user_id)]

    def update_order_status(self, order_id: UUID, status_value: OrderStatus) -> OrderResponse:
        order = self.order_repository.update_status(order_id, status_value)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return self._to_response(order)

    def _to_response(self, order) -> OrderResponse:
        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            status=order.status,
            total_amount=order.total_amount,
            items=[
                OrderItemResponse(
                    id=item.id,
                    product_id=item.product_id,
                    product_name=item.product_name,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                    total_price=item.unit_price * item.quantity,
                )
                for item in order.items
            ],
        )
