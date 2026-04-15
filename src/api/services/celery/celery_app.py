from celery import Celery
from src.config import settings

celery_instance = Celery(
    "logistics_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["src.api.services.celery.tasks"],
)

celery_instance.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
