import hashlib


def get_hash(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()


def test_ping(redisapi):
    response = redisapi.ping()

    assert response is True


def test_encoding(redisapi):
    redis = redisapi.get_redis()

    redis.set('a', 'b')
    result = redis.get('a')

    assert result == 'b'


def test_add_textjob(redisapi):
    redis = redisapi.get_redis()
    job_type = 'text'
    job_url = 'http://www.lipsum.com'
    job_hash = get_hash(job_type + job_url)

    result = redis.hget('jobs', job_hash)
    assert result is None

    result, status = redisapi.add_job(job_type=job_type, job_url=job_url)
    assert result == job_hash
    assert status == 1

    result = redis.hget('jobs', job_hash)
    assert result == '1'


def test_add_imagejob(redisapi):
    redis = redisapi.get_redis()
    job_type = 'images'
    job_url = 'http://www.lipsum.com'
    job_hash = get_hash(job_type + job_url)

    result = redis.hget('jobs', job_hash)
    assert result is None

    result, status = redisapi.add_job(job_type=job_type, job_url=job_url)
    assert result == job_hash
    assert status == 1

    result = redis.hget('jobs', job_hash)
    assert result == '1'


def test_check_status_textjob(redisapi):
    redis = redisapi.get_redis()
    job_type = 'text'
    job_url = 'http://www.lipsum.com'
    job_hash = get_hash(job_type + job_url)

    result = redisapi.get_status(job_hash='invald_hash')
    assert result == 'not found'

    redis.hset('jobs', job_hash, -1)
    result = redisapi.get_status(job_hash=job_hash)
    assert result == 'invalid URL error'

    redis.hset('jobs', job_hash, 1)
    result = redisapi.get_status(job_hash=job_hash)
    assert result == 'pending'

    redis.hset('jobs', job_hash, 2)
    result = redisapi.get_status(job_hash=job_hash)
    assert result == 'done'


def test_check_status_imagejob(redisapi):
    redis = redisapi.get_redis()
    job_type = 'images'
    job_url = 'http://www.lipsum.com'
    job_hash = get_hash(job_type + job_url)

    result = redisapi.get_status(job_hash='invald_hash')
    assert result == 'not found'

    redis.hset('jobs', job_hash, -1)
    result = redisapi.get_status(job_hash=job_hash)
    assert result == 'invalid URL error'

    redis.hset('jobs', job_hash, 1)
    result = redisapi.get_status(job_hash=job_hash)
    assert result == 'pending'

    redis.hset('jobs', job_hash, 2)
    result = redisapi.get_status(job_hash=job_hash)
    assert result == 'done'
