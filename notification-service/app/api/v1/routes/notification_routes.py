from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.application.use_cases.get_notification_logs import GetNotificationLogsUseCase
from app.dependencies import get_db, get_notification_logs_use_case
from app.schemas.notification_schema import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationResponse])
def list_notifications(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
):
    use_case: GetNotificationLogsUseCase = get_notification_logs_use_case(db)
    return use_case.list_all(skip=skip, limit=limit)


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification_by_id(
    notification_id: str,
    db: Session = Depends(get_db),
):
    use_case: GetNotificationLogsUseCase = get_notification_logs_use_case(db)
    notification = use_case.get_by_id(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    return notification


@router.get("/user/{user_id}/logs", response_model=list[NotificationResponse])
def list_notifications_by_user_id(
    user_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
):
    use_case: GetNotificationLogsUseCase = get_notification_logs_use_case(db)
    return use_case.list_by_user_id(user_id=user_id, skip=skip, limit=limit)
