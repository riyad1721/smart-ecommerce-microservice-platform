from fastapi import HTTPException, status

from app.domain.entities.payment import PaymentStatus
from app.infrastructure.repositories.payment_repository import PaymentRepository


class UpdatePaymentStatusUseCase:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def execute(
        self,
        payment_id: str,
        new_status: PaymentStatus,
        failure_reason: str | None = None,
    ):
        payment = self.repository.get_by_id(payment_id)

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found",
            )

        return self.repository.update_status(payment, new_status, failure_reason)