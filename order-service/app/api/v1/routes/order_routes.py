from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.services.order_service import OrderService
from app.dependencies import get_current_user_id, get_order_service
from app.schemas.order_schema import OrderResponse, UpdateOrderStatusRequest

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    user_id: str = Depends(get_current_user_id),
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.create_order_from_cart(user_id)


@router.get("", response_model=list[OrderResponse])
def list_my_orders(
    user_id: str = Depends(get_current_user_id),
    order_service: OrderService = Depends(get_order_service),
):
    return order_service.list_user_orders(user_id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: UUID,
    user_id: str = Depends(get_current_user_id),
    order_service: OrderService = Depends(get_order_service),
):
    return order_service.get_order(order_id, user_id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status_for_learning(
    order_id: UUID,
    request: UpdateOrderStatusRequest,
    order_service: OrderService = Depends(get_order_service),
    user_id: str = Depends(get_current_user_id),
):
    # In real production, this endpoint should be admin/internal only.
    return order_service.update_order_status(order_id, request.status)
