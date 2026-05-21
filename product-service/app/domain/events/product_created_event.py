from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProductCreatedEvent:
    product_id: int
    name: str
    price: Decimal
    stock: int
    category_id: int

    def to_dict(self) -> dict:
        return {
            "event": "product.created",
            "product_id": self.product_id,
            "name": self.name,
            "price": str(self.price),
            "stock": self.stock,
            "category_id": self.category_id,
        }