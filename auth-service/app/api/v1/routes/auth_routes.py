from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.services.auth_service import AuthService
from app.infrastructure.database.session import get_db_session
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.message_broker.rabbitmq_publisher import RabbitMQPublisher
from app.schemas.user_schema import UserRegisterRequest, UserLoginRequest, UserResponse
from app.schemas.token_schema import TokenResponse


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db_session)
):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)

    user = auth_service.register_user(
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password
    )

    publisher = RabbitMQPublisher()

    await publisher.publish_user_registered(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name
    )

    return user


@router.post("/login", response_model=TokenResponse)
def login_user(
    payload: UserLoginRequest,
    db: Session = Depends(get_db_session)
):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)

    access_token = auth_service.login_user(
        email=payload.email,
        password=payload.password
    )

    return TokenResponse(access_token=access_token)