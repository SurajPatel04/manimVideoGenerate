import redis
from app.config import Config

REDIS_URL = Config.REDIS_URL
r = redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_KEY = "celery"

def get_queue_length():
    return r.llen(QUEUE_KEY)
