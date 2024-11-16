import socket
import redis
from redis import Redis, ConnectionPool
from redis.exceptions import RedisError
import logging
from app.core.config import settings
from typing import Optional, Union

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        try:
            if settings.REDIS_URL:
                self.pool = ConnectionPool.from_url(
                    settings.REDIS_URL,
                    socket_timeout=5.0,
                    password=settings.REDIS_PASSWORD,
                    socket_connect_timeout=5.0,
                    retry_on_timeout=True,
                    max_connections=10,
                )
            else:
                self.pool = ConnectionPool(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    socket_timeout=5.0,
                    socket_connect_timeout=5.0,
                    retry_on_timeout=True,
                    max_connections=10,
                )

            self.client = Redis(connection_pool=self.pool)
            # Test connection
            self.client.ping()
        except RedisError as e:
            logger.error(f"Failed to initialize Redis connection: {str(e)}")
            # Initialize client as None, but don't raise error to allow fallback behavior
            self.client = None

    def get(self, key: str) -> Optional[bytes]:
        """
        Get value from Redis with error handling
        """
        if not self.client:
            logger.warning("Redis client not initialized, skipping get operation")
            return None

        try:
            return self.client.get(key)
        except RedisError as e:
            logger.error(f"Redis get error for key {key}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in Redis get operation: {str(e)}")
            return None

    def set(self, key: str, value: Union[str, bytes], expire: int = 3600) -> bool:
        """
        Set value in Redis with error handling
        """
        if not self.client:
            logger.warning("Redis client not initialized, skipping set operation")
            return False

        try:
            return bool(self.client.set(key, value, ex=expire))
        except RedisError as e:
            logger.error(f"Redis set error for key {key}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in Redis set operation: {str(e)}")
            return False

    def close(self) -> None:
        """
        Safely close Redis connection
        """
        try:
            if self.client:
                self.client.close()
        except Exception as e:
            logger.error(f"Error while closing Redis connection: {str(e)}")
