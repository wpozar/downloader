import hashlib

from flask import current_app
from redis import ConnectionPool, Redis
from rq import Queue


class RedisApi(object):
    """Singleton for redis api instance"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(cls.__class__, cls).__new__(cls)
        return cls._instance

    def __init__(self, redis_url=None):
        if not redis_url:
            redis_url = current_app.config.get('REDIS_URL', 'redis://redis:6379/0')
        self._redis_pool = ConnectionPool.from_url(redis_url, decode_responses=True)
        self._redis = Redis(connection_pool=self._redis_pool)
        self._queue = Queue('tasks', connection=self._redis)

    def get_redis(self):
        return self._redis

    def ping(self):
        return self._redis.ping()

    def get_hash(self, value):
        return hashlib.md5(value.encode('utf-8')).hexdigest()

    def add_job(self, job_type, job_url):
        job_hash = self.get_hash(value=job_type + job_url)
        result = self._redis.hsetnx('jobs', job_hash, 1)

        if result is 1:
            args = (job_type, job_url, job_hash)
            self._queue.enqueue_call('worker.get_website', args=args)

        return job_hash, result

    def get_status(self, job_hash):
        result = self._redis.hget('jobs', job_hash)
        if not result:
            result = '0'

        results = {
            '-1': 'invalid URL error',
            '0': 'not found',
            '1': 'pending',
            '2': 'done'
        }

        return results[result]
