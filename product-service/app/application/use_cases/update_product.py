from app.application.services.product_service import ProductService
from app.schemas.product_schema import ProductUpdate


class UpdateProductUseCase:
    def __init__(self, service: ProductService):
        self.service = service

    def execute(self, product_id: int, data: ProductUpdate):
        return self.service.update_product(product_id, data)