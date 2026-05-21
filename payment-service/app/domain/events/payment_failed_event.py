from decimal import Decimal
from pydantic import BaseModel


class PaymentFailedEvent(BaseModel):
    event_type: str = "payment.failed"
    payment_id: str
    order_id: str
    user_id: str
    amount: Decimal
    currency: str
    status: str
    reason: str