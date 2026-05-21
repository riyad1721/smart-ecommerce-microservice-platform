from app.application.services.cart_service import CartService
from app.schemas.cart_schema import CartResponse


class RemoveFromCartUseCase:
    def __init__(self, cart_service: CartService):
        self.cart_service = cart_service

    def execute(self, user_id: str, product_id: str) -> CartResponse:
        return self.cart_service.remove_from_cart(user_id, product_id)
