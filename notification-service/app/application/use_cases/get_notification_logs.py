from app.infrastructure.repositories.notification_repository import NotificationRepository


class GetNotificationLogsUseCase:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def list_all(self, skip: int = 0, limit: int = 100):
        return self.repository.list_all(skip=skip, limit=limit)

    def get_by_id(self, notification_id: str):
        return self.repository.get_by_id(notification_id)

    def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100):
        return self.repository.list_by_user_id(
            user_id=user_id,
            skip=skip,
            limit=limit,
        )
