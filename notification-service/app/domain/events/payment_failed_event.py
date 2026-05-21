from typing import Optional
from pydantic import BaseModel


class PaymentFailedEvent(BaseModel):
    event_id: Optional[str] = None
    user_id: str
    order_id: Optional[str] = None
    payment_id: Optional[str] = None
    email: Optional[str] = None
    reason: Optional[str] = None
