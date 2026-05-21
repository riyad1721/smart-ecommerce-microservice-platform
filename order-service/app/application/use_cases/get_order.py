from uuid import UUID

from app.application.services.order_service import OrderService
from app.schemas.order_schema import OrderResponse


class GetOrderUseCase:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def execute(self, order_id: UUID, user_id: str) -> OrderResponse:
        return self.order_service.get_order(order_id, user_id)
