from uuid import UUID
from pydantic import BaseModel


class PaymentCompletedEvent(BaseModel):
    event_type: str = "payment.completed"
    order_id: UUID
