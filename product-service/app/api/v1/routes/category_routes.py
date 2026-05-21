from fastapi import APIRouter, Depends
from app.dependencies import get_product_service, get_current_user
from app.application.services.product_service import ProductService
from app.schemas.category_schema import CategoryCreate, CategoryResponse


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "",
    response_model=CategoryResponse,
    dependencies=[Depends(get_current_user)],
)
def create_category(
    data: CategoryCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.create_category(data)


@router.get("", response_model=list[CategoryResponse])
def list_categories(
    service: ProductService = Depends(get_product_service),
):
    return service.list_categories()