from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel


class OrderCreatedEvent(BaseModel):
    event_type: str = "order.created"
    order_id: UUID
    user_id: str
    total_amount: Decimal
