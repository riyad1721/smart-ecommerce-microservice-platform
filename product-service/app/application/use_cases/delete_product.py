from app.application.services.product_service import ProductService


class DeleteProductUseCase:
    def __init__(self, service: ProductService):
        self.service = service

    def execute(self, product_id: int):
        return self.service.delete_product(product_id)