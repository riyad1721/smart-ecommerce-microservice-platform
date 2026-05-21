from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db_session
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.services.auth_service import AuthService


def get_user_repository(db: Session) -> UserRepository:
    return UserRepository(db)


def get_auth_service(db: Session) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)