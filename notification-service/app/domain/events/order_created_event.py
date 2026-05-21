from typing import Optional
from pydantic import BaseModel


class OrderCreatedEvent(BaseModel):
    event_id: Optional[str] = None
    user_id: str
    order_id: str
    email: Optional[str] = None
    total_amount: Optional[float] = None
