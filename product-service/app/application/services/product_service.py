import asyncio
import threading

from fastapi import HTTPException

from app.infrastructure.repositories.product_repository import ProductRepository
from app.infrastructure.message_broker.rabbitmq_publisher import RabbitMQPublisher

from app.schemas.product_schema import ProductCreate, ProductUpdate

from app.schemas.category_schema import CategoryCreate

from app.domain.events.product_created_event import ProductCreatedEvent
from app.domain.events.stock_updated_event import StockUpdatedEvent


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository
        self.publisher = RabbitMQPublisher()

    def _publish_background(self, routing_key: str, message: dict):
        """
        Run RabbitMQ publish in background thread.
        Prevent API failure if RabbitMQ is down.
        """

        def runner():
            try:
                asyncio.run(
                    self.publisher.publish(routing_key, message)
                )
            except Exception:
                pass

        thread = threading.Thread(target=runner, daemon=True)
        thread.start()

    def create_category(self, data: CategoryCreate):
        return self.repository.create_category(data)

    def list_categories(self):
        return self.repository.list_categories()

    def create_product(self, data: ProductCreate):

        category = self.repository.get_category(data.category_id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        product = self.repository.create_product(data)

        event = ProductCreatedEvent(
            product_id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category_id=product.category_id,
        )

        self._publish_background(
            "product.created",
            event.to_dict(),
        )

        return product

    def update_product(self, product_id: int, data: ProductUpdate):

        product = self.repository.get_product(product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        old_stock = product.stock

        if data.category_id:

            category = self.repository.get_category(data.category_id)

            if not category:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found",
                )

        updated_product = self.repository.update_product(
            product,
            data,
        )

        if (
            data.stock is not None
            and data.stock != old_stock
        ):

            event = StockUpdatedEvent(
                product_id=updated_product.id,
                old_stock=old_stock,
                new_stock=updated_product.stock,
            )

            self._publish_background(
                "stock.updated",
                event.to_dict(),
            )

        return updated_product

    def update_stock(self, product_id: int, new_stock: int):

        product = self.repository.get_product(product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        old_stock = product.stock

        updated_product = self.repository.update_product(
            product,
            ProductUpdate(stock=new_stock),
        )

        event = StockUpdatedEvent(
            product_id=updated_product.id,
            old_stock=old_stock,
            new_stock=new_stock,
        )

        self._publish_background(
            "stock.updated",
            event.to_dict(),
        )

        return updated_product

    def delete_product(self, product_id: int):

        product = self.repository.get_product(product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        self.repository.delete_product(product)

        return {
            "message": "Product deleted successfully"
        }

    def get_product(self, product_id: int):

        product = self.repository.get_product(product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return product

    def list_products(self, category_id: int | None = None):
        return self.repository.list_products(category_id)

    def search_products(self, name: str):
        return self.repository.search_products(name)