from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class CartItemEntity:
    id: UUID
    cart_id: UUID
    product_id: str
    product_name: str
    unit_price: Decimal
    quantity: int

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity
