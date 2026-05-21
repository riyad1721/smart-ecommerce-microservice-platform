from app.application.services.notification_service import NotificationService
from app.domain.entities.notification import NotificationType
from app.domain.events.order_created_event import OrderCreatedEvent


class SendOrderNotificationUseCase:
    def __init__(self, service: NotificationService):
        self.service = service

    def execute(self, event: OrderCreatedEvent):
        subject = "Order Created Successfully"
        message = f"Your order {event.order_id} has been created successfully."

        if event.total_amount is not None:
            message += f" Total amount: {event.total_amount}."

        return self.service.send_notification(
            event_id=event.event_id,
            user_id=event.user_id,
            notification_type=NotificationType.ORDER_CREATED,
            recipient_email=event.email,
            subject=subject,
            message=message,
            payload=event.model_dump(),
        )
