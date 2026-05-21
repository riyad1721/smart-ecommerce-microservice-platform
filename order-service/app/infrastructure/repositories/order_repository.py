from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.entities.order import OrderStatus
from app.infrastructure.database.models import OrderModel, OrderItemModel


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_from_cart(self, user_id: str, cart_items: list) -> OrderModel:
        total_amount = sum(item.unit_price * item.quantity for item in cart_items)

        order = OrderModel(
            user_id=user_id,
            status=OrderStatus.PAYMENT_PENDING,
            total_amount=total_amount,
        )
        self.db.add(order)
        self.db.flush()

        for item in cart_items:
            self.db.add(
                OrderItemModel(
                    order_id=order.id,
                    product_id=item.product_id,
                    product_name=item.product_name,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                )
            )

        self.db.commit()
        return self.get_by_id(order.id)

    def get_by_id(self, order_id: UUID) -> OrderModel | None:
        stmt = (
            select(OrderModel)
            .where(OrderModel.id == order_id)
            .options(selectinload(OrderModel.items))
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_id_and_user_id(self, order_id: UUID, user_id: str) -> OrderModel | None:
        stmt = (
            select(OrderModel)
            .where(OrderModel.id == order_id, OrderModel.user_id == user_id)
            .options(selectinload(OrderModel.items))
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_by_user_id(self, user_id: str) -> list[OrderModel]:
        stmt = (
            select(OrderModel)
            .where(OrderModel.user_id == user_id)
            .options(selectinload(OrderModel.items))
            .order_by(OrderModel.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def update_status(self, order_id: UUID, status: OrderStatus) -> OrderModel | None:
        order = self.get_by_id(order_id)
        if not order:
            return None

        order.status = status
        self.db.commit()
        return self.get_by_id(order_id)
