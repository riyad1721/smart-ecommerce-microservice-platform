from decimal import Decimal
from pydantic import BaseModel


class PaymentCompletedEvent(BaseModel):
    event_type: str = "payment.completed"
    payment_id: str
    order_id: str
    user_id: str
    amount: Decimal
    currency: str
    status: str