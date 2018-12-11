import os

from redis import ConnectionPool, Redis

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')

redis_pool = ConnectionPool.from_url(redis_url)
redis = Redis(connection_pool=redis_pool)
