from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from uuid import UUID


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAID = "PAID"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class OrderEntity:
    id: UUID
    user_id: str
    status: OrderStatus
    total_amount: Decimal
    items: list = field(default_factory=list)