import pytest

from api import create_app
from api.redisapi import RedisApi


@pytest.fixture
def client():
    config = {
        'ENV': 'testing',
        'DEBUG': False,
        'TESTING': True,
        'REDIS_URL': 'redis://redis:6379/1'
    }

    app = create_app(config=config)
    client = app.test_client()

    return client


@pytest.fixture
def redisapi():
    redis_url = "redis://redis:6379/1"

    # setup
    redisapi = RedisApi(redis_url=redis_url)

    yield redisapi

    # cleanup
    redisapi.get_redis().flushdb()
