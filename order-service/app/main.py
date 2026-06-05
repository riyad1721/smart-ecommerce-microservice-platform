import asyncio
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routes import cart_routes, health_routes, order_routes
from app.core.config import settings
from app.core.logging import configure_logging
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine

# Important: import models before create_all()
from app.infrastructure.database import models  # noqa: F401
from app.infrastructure.message_broker.rabbitmq_consumer import start_payment_event_consumer
from fastapi.middleware.cors import CORSMiddleware

configure_logging()
logger = logging.getLogger(__name__)


def create_database_tables() -> None:
    for attempt in range(1, 11):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created/verified.")
            return
        except Exception:
            logger.exception("Database table creation failed on attempt %s/10.", attempt)
            if attempt == 10:
                raise
            time.sleep(3)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()

    consumer_task = None
    if settings.ENABLE_RABBITMQ_CONSUMER:
        consumer_task = asyncio.create_task(start_payment_event_consumer())

    yield

    if consumer_task:
        consumer_task.cancel()


app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(cart_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(order_routes.router, prefix=settings.API_V1_PREFIX)
