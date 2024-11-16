import redis
from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
        )

    def get(self, key: str):
        return self.client.get(key)

    def set(self, key: str, value: str):
        self.client.set(key, value)
