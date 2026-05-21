from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.dependencies import get_payment_repository, get_payment_service
from app.infrastructure.repositories.payment_repository import PaymentRepository
from app.application.services.payment_service import PaymentService
from app.application.use_cases.get_payment import GetPaymentUseCase
from app.application.use_cases.process_payment import ProcessPaymentUseCase
from app.application.use_cases.update_payment_status import UpdatePaymentStatusUseCase
from app.schemas.payment_schema import (
    CreatePaymentRequest,
    ProcessPaymentRequest,
    UpdatePaymentStatusRequest,
    PaymentResponse,
)

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])


@router.post("", response_model=PaymentResponse)
def create_payment_manually(
    request: CreatePaymentRequest,
    current_user: dict = Depends(get_current_user),
    repository: PaymentRepository = Depends(get_payment_repository),
):
    payment = repository.create_payment(
        order_id=request.order_id,
        user_id=current_user["user_id"],
        amount=request.amount,
        currency=request.currency,
    )
    return payment


@router.post("/{payment_id}/process", response_model=PaymentResponse)
async def process_payment(
    payment_id: str,
    request: ProcessPaymentRequest,
    current_user: dict = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
):
    use_case = ProcessPaymentUseCase(service)
    return await use_case.execute(payment_id, request.force_result)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment_by_id(
    payment_id: str,
    current_user: dict = Depends(get_current_user),
    repository: PaymentRepository = Depends(get_payment_repository),
):
    use_case = GetPaymentUseCase(repository)
    return use_case.get_by_id(payment_id)


@router.get("/order/{order_id}", response_model=PaymentResponse)
def get_payment_by_order_id(
    order_id: str,
    current_user: dict = Depends(get_current_user),
    repository: PaymentRepository = Depends(get_payment_repository),
):
    use_case = GetPaymentUseCase(repository)
    return use_case.get_by_order_id(order_id)


@router.get("", response_model=list[PaymentResponse])
def list_my_payments(
    current_user: dict = Depends(get_current_user),
    repository: PaymentRepository = Depends(get_payment_repository),
):
    use_case = GetPaymentUseCase(repository)
    return use_case.list_by_user(current_user["user_id"])


@router.patch("/{payment_id}/status", response_model=PaymentResponse)
def update_payment_status(
    payment_id: str,
    request: UpdatePaymentStatusRequest,
    current_user: dict = Depends(get_current_user),
    repository: PaymentRepository = Depends(get_payment_repository),
):
    use_case = UpdatePaymentStatusUseCase(repository)
    return use_case.execute(
        payment_id=payment_id,
        new_status=request.status,
        failure_reason=request.failure_reason,
    )