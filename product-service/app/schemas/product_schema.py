from decimal import Decimal
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category_id: int


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    category_id: int | None = None


class StockUpdate(BaseModel):
    stock: int = Field(..., ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: Decimal
    stock: int
    category_id: int

    model_config = {"from_attributes": True}