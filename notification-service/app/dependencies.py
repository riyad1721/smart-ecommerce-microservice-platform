from collections.abc import Generator

from sqlalchemy.orm import Session

from app.application.services.notification_service import NotificationService
from app.application.use_cases.get_notification_logs import GetNotificationLogsUseCase
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.notification_repository import NotificationRepository


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_notification_repository(db: Session) -> NotificationRepository:
    return NotificationRepository(db)


def get_notification_service(db: Session) -> NotificationService:
    repository = NotificationRepository(db)
    return NotificationService(repository)


def get_notification_logs_use_case(db: Session) -> GetNotificationLogsUseCase:
    repository = NotificationRepository(db)
    return GetNotificationLogsUseCase(repository)
