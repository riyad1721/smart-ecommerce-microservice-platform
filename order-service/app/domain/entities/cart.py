from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID


@dataclass
class CartEntity:
    id: UUID
    user_id: str
    items: list = field(default_factory=list)

    @property
    def total_amount(self) -> Decimal:
        return sum((item.total_price for item in self.items), Decimal("0.00"))
