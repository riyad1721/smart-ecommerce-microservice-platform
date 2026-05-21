from app.application.services.cart_service import CartService
from app.schemas.cart_schema import AddToCartRequest, CartResponse


class AddToCartUseCase:
    def __init__(self, cart_service: CartService):
        self.cart_service = cart_service

    async def execute(self, user_id: str, request: AddToCartRequest) -> CartResponse:
        return await self.cart_service.add_to_cart(user_id, request)
