from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    product_id: str = Field(..., examples=["product-1"])
    quantity: int = Field(..., gt=0, examples=[2])


class CartItemResponse(BaseModel):
    id: UUID
    product_id: str
    product_name: str
    unit_price: Decimal
    quantity: int
    total_price: Decimal


class CartResponse(BaseModel):
    id: UUID | None = None
    user_id: str
    items: list[CartItemResponse] = []
    total_amount: Decimal = Decimal("0.00")
