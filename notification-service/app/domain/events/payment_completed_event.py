from typing import Optional
from pydantic import BaseModel


class PaymentCompletedEvent(BaseModel):
    event_id: Optional[str] = None
    user_id: str
    order_id: Optional[str] = None
    payment_id: str
    email: Optional[str] = None
    amount: Optional[float] = None
