from fastapi import APIRouter, Depends, status

from app.application.services.cart_service import CartService
from app.dependencies import get_cart_service, get_current_user_id
from app.schemas.cart_schema import AddToCartRequest, CartResponse

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    request: AddToCartRequest,
    user_id: str = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    return await cart_service.add_to_cart(user_id, request)


@router.get("", response_model=CartResponse)
def view_cart(
    user_id: str = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    return cart_service.view_cart(user_id)


@router.delete("/items/{product_id}", response_model=CartResponse)
def remove_from_cart(
    product_id: str,
    user_id: str = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    return cart_service.remove_from_cart(user_id, product_id)
