from uuid import UUID

from app.application.services.order_service import OrderService
from app.domain.entities.order import OrderStatus
from app.schemas.order_schema import OrderResponse


class UpdateOrderStatusUseCase:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def execute(self, order_id: UUID, status: OrderStatus) -> OrderResponse:
        return self.order_service.update_order_status(order_id, status)
