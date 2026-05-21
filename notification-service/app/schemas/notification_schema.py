from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.domain.entities.notification import NotificationStatus, NotificationType


class NotificationResponse(BaseModel):
    id: str
    event_id: str | None
    user_id: str
    notification_type: NotificationType
    status: NotificationStatus
    recipient_email: str | None
    subject: str
    message: str
    payload: dict[str, Any] | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
