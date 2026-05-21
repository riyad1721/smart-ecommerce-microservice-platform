from app.application.services.order_service import OrderService
from app.schemas.order_schema import OrderResponse


class CreateOrderUseCase:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    async def execute(self, user_id: str) -> OrderResponse:
        return await self.order_service.create_order_from_cart(user_id)
