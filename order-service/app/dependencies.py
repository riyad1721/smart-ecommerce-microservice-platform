from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.application.services.cart_service import CartService
from app.application.services.order_service import OrderService
from app.core.security import bearer_scheme, decode_access_token
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.external_clients.product_client import ProductClient
from app.infrastructure.message_broker.rabbitmq_publisher import RabbitMQPublisher
from app.infrastructure.repositories.cart_repository import CartRepository
from app.infrastructure.repositories.order_repository import OrderRepository


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    payload = decode_access_token(credentials.credentials)
    return str(payload["sub"])


def get_cart_service(db: Session = Depends(get_db)) -> CartService:
    return CartService(
        cart_repository=CartRepository(db),
        product_client=ProductClient(),
    )


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(
        cart_repository=CartRepository(db),
        order_repository=OrderRepository(db),
        publisher=RabbitMQPublisher(),
    )
