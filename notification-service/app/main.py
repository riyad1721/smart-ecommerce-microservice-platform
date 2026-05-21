import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routes import health_routes, notification_routes
from app.core.config import settings
from app.core.logging import setup_logging
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine
from app.infrastructure.message_broker.rabbitmq_consumer import start_rabbitmq_consumer

# Important: import models before Base.metadata.create_all()
from app.infrastructure.database import models  # noqa: F401
from fastapi.middleware.cors import CORSMiddleware

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting notification-service")

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created or already exist")

    if settings.RABBITMQ_ENABLED:
        asyncio.create_task(start_rabbitmq_consumer())
        logger.info("RabbitMQ consumer scheduled in background")

    yield

    logger.info("Stopping notification-service")


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

app.include_router(health_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(notification_routes.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
    }
