from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    id: int | None
    name: str
    description: str | None
    price: Decimal
    stock: int
    category_id: int