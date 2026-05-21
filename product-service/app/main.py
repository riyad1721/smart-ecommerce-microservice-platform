from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine

# Important: import SQLAlchemy models before create_all()
from app.infrastructure.database import models  # noqa: F401

from app.api.v1.routes import product_routes, category_routes, health_routes
from fastapi.middleware.cors import CORSMiddleware


setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

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