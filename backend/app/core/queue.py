from celery import Celery
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

# It's crucial to load environment variables before they are used.
BROKER_URL = os.getenv("REDIS_URL")

if not BROKER_URL:
    raise ValueError("REDIS_URL environment variable not set. Please create a .env file.")

# This file now only defines and configures the Celery application.
# The `include` parameter tells Celery where to find your task definitions.
taskQueue = Celery(
    "taskQueue",
    broker=BROKER_URL,
    backend=BROKER_URL,
    # --- THIS IS THE FIX ---
    # We are now providing the full Python path to your tasks file.
    # Celery will look for 'app/services/task.py' relative to your project root.
    include=["app.services.manim"] 
)

# Apply SSL configuration if you are connecting to a secured Redis instance
taskQueue.conf.update(
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    # It's good practice to have tasks acknowledge they've started.
    task_acks_late = True,
    worker_prefetch_multiplier = 1
)
