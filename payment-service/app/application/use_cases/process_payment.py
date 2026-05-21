from app.application.services.payment_service import PaymentService


class ProcessPaymentUseCase:
    def __init__(self, service: PaymentService):
        self.service = service

    async def execute(self, payment_id: str, force_result: str | None = None):
        return await self.service.process_payment(payment_id, force_result)