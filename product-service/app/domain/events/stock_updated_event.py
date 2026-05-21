from dataclasses import dataclass


@dataclass
class StockUpdatedEvent:
    product_id: int
    old_stock: int
    new_stock: int

    def to_dict(self) -> dict:
        return {
            "event": "stock.updated",
            "product_id": self.product_id,
            "old_stock": self.old_stock,
            "new_stock": self.new_stock,
        }