import logging
from typing import Any

from app.domain.entities.notification import NotificationStatus, NotificationType
from app.infrastructure.database.models import NotificationModel
from app.infrastructure.repositories.notification_repository import NotificationRepository

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def send_notification(
        self,
        event_id: str | None,
        user_id: str,
        notification_type: NotificationType,
        recipient_email: str | None,
        subject: str,
        message: str,
        payload: dict[str, Any] | None = None,
    ) -> NotificationModel:
        if event_id:
            existing = self.repository.get_by_event_id(event_id)
            if existing:
                logger.info("Duplicate event ignored. event_id=%s", event_id)
                return existing

        notification = NotificationModel(
            event_id=event_id,
            user_id=user_id,
            notification_type=notification_type.value,
            status=NotificationStatus.PENDING.value,
            recipient_email=recipient_email,
            subject=subject,
            message=message,
            payload=payload,
        )

        notification = self.repository.create(notification)

        try:
            self._simulate_email_send(notification)
            return self.repository.update_status(
                notification,
                NotificationStatus.SENT.value,
            )
        except Exception as exc:
            logger.exception("Notification sending failed")
            return self.repository.update_status(
                notification,
                NotificationStatus.FAILED.value,
                str(exc),
            )

    def _simulate_email_send(self, notification: NotificationModel) -> None:
        logger.info("========== EMAIL SIMULATION ==========")
        logger.info("To: %s", notification.recipient_email or "unknown@example.com")
        logger.info("Subject: %s", notification.subject)
        logger.info("Message: %s", notification.message)
        logger.info("Notification Type: %s", notification.notification_type)
        logger.info("======================================")
