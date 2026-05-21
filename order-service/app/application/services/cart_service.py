from decimal import Decimal

from fastapi import HTTPException, status

from app.infrastructure.external_clients.product_client import ProductClient
from app.infrastructure.repositories.cart_repository import CartRepository
from app.schemas.cart_schema import AddToCartRequest, CartResponse, CartItemResponse


class CartService:
    def __init__(self, cart_repository: CartRepository, product_client: ProductClient):
        self.cart_repository = cart_repository
        self.product_client = product_client

    async def add_to_cart(self, user_id: str, request: AddToCartRequest) -> CartResponse:
        product = await self.product_client.get_product(request.product_id)

        if product.stock is not None and product.stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough product stock",
            )

        cart = self.cart_repository.get_or_create_by_user_id(user_id)
        updated_cart = self.cart_repository.add_item(
            cart=cart,
            product_id=product.id,
            product_name=product.name,
            unit_price=product.price,
            quantity=request.quantity,
        )
        return self._to_response(updated_cart)

    def view_cart(self, user_id: str) -> CartResponse:
        cart = self.cart_repository.get_by_user_id(user_id)
        if not cart:
            return CartResponse(user_id=user_id, items=[], total_amount=Decimal("0.00"))
        return self._to_response(cart)

    def remove_from_cart(self, user_id: str, product_id: str) -> CartResponse:
        cart = self.cart_repository.remove_item(user_id, product_id)
        if not cart:
            return CartResponse(user_id=user_id, items=[], total_amount=Decimal("0.00"))
        return self._to_response(cart)

    def clear_cart(self, user_id: str) -> None:
        self.cart_repository.clear_cart(user_id)

    def _to_response(self, cart) -> CartResponse:
        items = [
            CartItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total_price=item.unit_price * item.quantity,
            )
            for item in cart.items
        ]
        total_amount = sum((item.total_price for item in items), Decimal("0.00"))
        return CartResponse(id=cart.id, user_id=cart.user_id, items=items, total_amount=total_amount)
