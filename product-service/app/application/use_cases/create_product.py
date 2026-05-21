from app.application.services.product_service import ProductService
from app.schemas.product_schema import ProductCreate


class CreateProductUseCase:
    def __init__(self, service: ProductService):
        self.service = service

    def execute(self, data: ProductCreate):
        return self.service.create_product(data)