from sqlalchemy.orm import Session

from app.infrastructure.database.models import NotificationModel


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, notification: NotificationModel) -> NotificationModel:
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_by_id(self, notification_id: str) -> NotificationModel | None:
        return (
            self.db.query(NotificationModel)
            .filter(NotificationModel.id == notification_id)
            .first()
        )

    def get_by_event_id(self, event_id: str) -> NotificationModel | None:
        return (
            self.db.query(NotificationModel)
            .filter(NotificationModel.event_id == event_id)
            .first()
        )

    def list_all(self, skip: int = 0, limit: int = 100) -> list[NotificationModel]:
        return (
            self.db.query(NotificationModel)
            .order_by(NotificationModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_user_id(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[NotificationModel]:
        return (
            self.db.query(NotificationModel)
            .filter(NotificationModel.user_id == user_id)
            .order_by(NotificationModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_status(
        self,
        notification: NotificationModel,
        status: str,
        error_message: str | None = None,
    ) -> NotificationModel:
        notification.status = status
        notification.error_message = error_message
        self.db.commit()
        self.db.refresh(notification)
        return notification
