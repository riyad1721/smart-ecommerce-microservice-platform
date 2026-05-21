import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.database.base import Base


class PaymentModel(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(String(100), nullable=False, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    status = Column(String(30), nullable=False, default="PENDING")
    failure_reason = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("order_id", name="uq_payments_order_id"),
    )