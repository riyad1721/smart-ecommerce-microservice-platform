from decimal import Decimal
from sqlalchemy.orm import Session

from app.infrastructure.database.models import PaymentModel
from app.domain.entities.payment import PaymentStatus


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(
        self,
        order_id: str,
        user_id: str,
        amount: Decimal,
        currency: str = "USD",
    ) -> PaymentModel:
        existing = self.get_by_order_id(order_id)
        if existing:
            return existing

        payment = PaymentModel(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.PENDING.value,
        )

        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_by_id(self, payment_id: str) -> PaymentModel | None:
        return self.db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()

    def get_by_order_id(self, order_id: str) -> PaymentModel | None:
        return self.db.query(PaymentModel).filter(PaymentModel.order_id == order_id).first()

    def list_by_user_id(self, user_id: str) -> list[PaymentModel]:
        return (
            self.db.query(PaymentModel)
            .filter(PaymentModel.user_id == user_id)
            .order_by(PaymentModel.created_at.desc())
            .all()
        )

    def update_status(
        self,
        payment: PaymentModel,
        status: PaymentStatus,
        failure_reason: str | None = None,
    ) -> PaymentModel:
        payment.status = status.value
        payment.failure_reason = failure_reason

        self.db.commit()
        self.db.refresh(payment)
        return payment