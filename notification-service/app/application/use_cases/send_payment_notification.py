from app.application.services.notification_service import NotificationService
from app.domain.entities.notification import NotificationType
from app.domain.events.payment_completed_event import PaymentCompletedEvent
from app.domain.events.payment_failed_event import PaymentFailedEvent


class SendPaymentCompletedNotificationUseCase:
    def __init__(self, service: NotificationService):
        self.service = service

    def execute(self, event: PaymentCompletedEvent):
        subject = "Payment Completed Successfully"
        message = f"Your payment {event.payment_id} has been completed successfully."

        if event.amount is not None:
            message += f" Paid amount: {event.amount}."

        return self.service.send_notification(
            event_id=event.event_id,
            user_id=event.user_id,
            notification_type=NotificationType.PAYMENT_COMPLETED,
            recipient_email=event.email,
            subject=subject,
            message=message,
            payload=event.model_dump(),
        )


class SendPaymentFailedNotificationUseCase:
    def __init__(self, service: NotificationService):
        self.service = service

    def execute(self, event: PaymentFailedEvent):
        subject = "Payment Failed"
        message = "Your payment has failed."

        if event.reason:
            message += f" Reason: {event.reason}."

        return self.service.send_notification(
            event_id=event.event_id,
            user_id=event.user_id,
            notification_type=NotificationType.PAYMENT_FAILED,
            recipient_email=event.email,
            subject=subject,
            message=message,
            payload=event.model_dump(),
        )
