from enum import Enum
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from datetime import datetime


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


@dataclass
class Payment:
    id: UUID
    order_id: str
    user_id: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    failure_reason: str | None
    created_at: datetime
    updated_at: datetime