from fastapi import FastAPI

from app.api.v1.routes import auth_routes, health_routes
from app.core.config import settings
from app.core.logging import configure_logging
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine

# Important: import models before create_all
from app.infrastructure.database import models
from fastapi.middleware.cors import CORSMiddleware



configure_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Authentication service for Smart E-Commerce Microservice Platform"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_routes.router, prefix="/api/v1")
app.include_router(auth_routes.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Auth Service is running"
    }