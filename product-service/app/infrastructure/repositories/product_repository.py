from sqlalchemy.orm import Session
from sqlalchemy import select
from app.infrastructure.database.models import ProductModel, CategoryModel
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.schemas.category_schema import CategoryCreate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, data: CategoryCreate) -> CategoryModel:
        category = CategoryModel(**data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def list_categories(self) -> list[CategoryModel]:
        return list(self.db.scalars(select(CategoryModel)).all())

    def get_category(self, category_id: int) -> CategoryModel | None:
        return self.db.get(CategoryModel, category_id)

    def create_product(self, data: ProductCreate) -> ProductModel:
        product = ProductModel(**data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_product(self, product_id: int) -> ProductModel | None:
        return self.db.get(ProductModel, product_id)

    def update_product(self, product: ProductModel, data: ProductUpdate) -> ProductModel:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product: ProductModel) -> None:
        self.db.delete(product)
        self.db.commit()

    def list_products(self, category_id: int | None = None) -> list[ProductModel]:
        query = select(ProductModel)

        if category_id:
            query = query.where(ProductModel.category_id == category_id)

        return list(self.db.scalars(query).all())

    def search_products(self, name: str) -> list[ProductModel]:
        query = select(ProductModel).where(ProductModel.name.ilike(f"%{name}%"))
        return list(self.db.scalars(query).all())