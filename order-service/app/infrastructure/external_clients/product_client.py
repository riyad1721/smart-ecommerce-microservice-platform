from decimal import Decimal

import httpx
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.core.config import settings


class ProductDTO(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int | None = None
    category_id: int | None = None


class ProductClient:
    def __init__(self) -> None:
        self.base_url = settings.PRODUCT_SERVICE_BASE_URL.rstrip("/")

    async def get_product(self, product_id: str) -> ProductDTO:
        url = f"{self.base_url}/api/v1/products/{product_id}"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Product service is unavailable",
            ) from exc

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Product service returned an error",
            )

        product = ProductDTO.model_validate(response.json())

        return product