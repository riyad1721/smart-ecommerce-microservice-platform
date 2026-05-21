from app.application.services.product_service import ProductService


class ListProductsUseCase:
    def __init__(self, service: ProductService):
        self.service = service

    def execute(self, category_id: int | None = None):
        return self.service.list_products(category_id)