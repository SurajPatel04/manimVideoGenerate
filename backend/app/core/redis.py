import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
r = redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_KEY = "celery"

def get_queue_length():
    return r.llen(QUEUE_KEY)
