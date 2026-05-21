from fastapi import APIRouter, Depends, Query
from app.dependencies import get_product_service, get_current_user
from app.application.services.product_service import ProductService
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse, StockUpdate


router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "",
    response_model=ProductResponse,
    dependencies=[Depends(get_current_user)],
)
def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.create_product(data)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    dependencies=[Depends(get_current_user)],
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    return service.update_product(product_id, data)


@router.patch(
    "/{product_id}/stock",
    response_model=ProductResponse,
    dependencies=[Depends(get_current_user)],
)
def update_stock(
    product_id: int,
    data: StockUpdate,
    service: ProductService = Depends(get_product_service),
):
    return service.update_stock(product_id, data.stock)


@router.delete(
    "/{product_id}",
    dependencies=[Depends(get_current_user)],
)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    return service.delete_product(product_id)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    return service.get_product(product_id)


@router.get("", response_model=list[ProductResponse])
def list_products(
    category_id: int | None = Query(default=None),
    service: ProductService = Depends(get_product_service),
):
    return service.list_products(category_id)


@router.get("/search/by-name", response_model=list[ProductResponse])
def search_products(
    name: str,
    service: ProductService = Depends(get_product_service),
):
    return service.search_products(name)