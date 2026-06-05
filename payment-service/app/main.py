import asyncio
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine

# Important: import models before create_all
from app.infrastructure.database import models  # noqa: F401

from app.api.v1.routes import health_routes, payment_routes
from app.infrastructure.message_broker.rabbitmq_consumer import start_rabbitmq_consumer
from fastapi.middleware.cors import CORSMiddleware

setup_logging()
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

    if settings.ENABLE_RABBITMQ_CONSUMER:
        asyncio.create_task(start_rabbitmq_consumer())

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_routes.router)
app.include_router(payment_routes.router)
