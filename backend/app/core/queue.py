from celery import Celery
import ssl
from app.config import Config

BROKER_URL = Config.REDIS_URL

if not BROKER_URL:
    raise ValueError("REDIS_URL environment variable not set. Please create a .env file.")

taskQueue = Celery(
    "taskQueue",
    broker=BROKER_URL,
    backend=BROKER_URL,
    include=["app.services.manim"] 
)

taskQueue.conf.update(
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    task_acks_late = True,
    worker_prefetch_multiplier = 1
)
