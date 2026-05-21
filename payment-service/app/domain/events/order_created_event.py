from decimal import Decimal
from pydantic import BaseModel


class OrderCreatedEvent(BaseModel):
    event_type: str = "order.created"
    order_id: str
    user_id: str
    amount: Decimal
    currency: str = "USD"