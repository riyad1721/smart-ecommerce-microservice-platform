from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.domain.entities.order import OrderStatus


class OrderItemResponse(BaseModel):
    id: UUID
    product_id: str
    product_name: str
    unit_price: Decimal
    quantity: int
    total_price: Decimal


class OrderResponse(BaseModel):
    id: UUID
    user_id: str
    status: OrderStatus
    total_amount: Decimal
    items: list[OrderItemResponse]


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus
