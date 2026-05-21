from decimal import Decimal
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.entities.payment import PaymentStatus


class CreatePaymentRequest(BaseModel):
    order_id: str
    amount: Decimal
    currency: str = "USD"


class ProcessPaymentRequest(BaseModel):
    force_result: str | None = None


class UpdatePaymentStatusRequest(BaseModel):
    status: PaymentStatus
    failure_reason: str | None = None


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: str
    user_id: str
    amount: Decimal
    currency: str
    status: str
    failure_reason: str | None = None
    created_at: datetime
    updated_at: datetime