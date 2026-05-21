from uuid import UUID
from pydantic import BaseModel


class PaymentFailedEvent(BaseModel):
    event_type: str = "payment.failed"
    order_id: UUID
    reason: str | None = None
