from fastapi import HTTPException, status

from app.infrastructure.repositories.payment_repository import PaymentRepository


class GetPaymentUseCase:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def get_by_id(self, payment_id: str):
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found",
            )
        return payment

    def get_by_order_id(self, order_id: str):
        payment = self.repository.get_by_order_id(order_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found for this order",
            )
        return payment

    def list_by_user(self, user_id: str):
        return self.repository.list_by_user_id(user_id)