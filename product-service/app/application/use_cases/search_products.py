from app.application.services.product_service import ProductService


class SearchProductsUseCase:
    def __init__(self, service: ProductService):
        self.service = service

    def execute(self, name: str):
        return self.service.search_products(name)