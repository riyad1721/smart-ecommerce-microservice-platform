import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import category_routes, health_routes, product_routes
from app.core.config import settings
from app.core.logging import setup_logging
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine

# Important: import SQLAlchemy models before create_all()
from app.infrastructure.database import models  # noqa: F401


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
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_routes.router, prefix="/api/v1")
app.include_router(category_routes.router, prefix="/api/v1")
app.include_router(product_routes.router, prefix="/api/v1")
