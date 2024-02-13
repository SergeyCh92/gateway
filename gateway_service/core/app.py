import logging

from fastapi import APIRouter, FastAPI

from gateway_service.routers import task_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - PID:%(process)d - threadName:%(thread)d - %(message)s",
)
logging.getLogger("pika").setLevel(logging.WARNING)

healthcheck_router = APIRouter(tags=["Health"])


@healthcheck_router.get("/")
def health_check():
    return {"status": "gateway_service is healthy"}


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(healthcheck_router)
    app.include_router(task_router)
    return app
