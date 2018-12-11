import hashlib


def get_hash(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()


def test_sanity():
    assert True


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data == {'response': 'pong'}


def test_error_handler_not_found(client):
    response = client.get('/invalid_request')
    assert response.status_code == 404


def test_invalid_job_no_postdata(client):
    response = client.post('/api/v1/job')
    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data == {
        'error': 'Request should contain "type" of [text|images] and "url".'
    }


def test_invalid_job_bad_postdata1(client):
    payload = {
        'url': 'https://google.com'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data == {
        'error': 'Request should contain "type" of [text|images] and "url".'
    }


def test_invalid_job_bad_postdata2(client):
    payload = {
        'type': 'invalid'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data == {
        'error': 'Request should contain "type" of [text|images] and "url".'
    }


def test_invalid_textjob_url(client):
    payload = {
        'type': 'text',
        'url': 'invalid_url'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data == {
        'error': 'Provided url is invalid.'
    }


def test_invalid_imagejob_url(client):
    payload = {
        'type': 'images',
        'url': 'invalid_url'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data == {
        'error': 'Provided url is invalid.'
    }


def test_textjob_request(client):
    payload = {
        'type': 'text',
        'url': 'http://www.lipsum.com'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code in (200, 201)

    job_hash = get_hash(payload['type'] + payload['url'])
    assert response.headers['location'] == '/api/v1/job/' + job_hash


def test_imagejob_request(client):
    payload = {
        'type': 'images',
        'url': 'http://www.lipsum.com'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code in (200, 201)

    job_hash = get_hash(payload['type'] + payload['url'])
    assert response.headers['location'] == '/api/v1/job/' + job_hash


def test_textjob_status(client):
    payload = {
        'type': 'text',
        'url': 'http://www.lipsum.com'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code in (200, 201)

    job_hash = get_hash(payload['type'] + payload['url'])
    location = '/api/v1/job/' + job_hash
    assert response.headers['location'] == location

    response = client.get(location)
    assert response.status_code == 200  # OK
    assert response.is_json
    data = response.get_json()
    assert 'status' in data
    assert data['status'] in ['invalid URL error', 'not found', 'pending', 'done']


def test_imagejob_status(client):
    payload = {
        'type': 'images',
        'url': 'http://www.lipsum.com'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code in (200, 201)

    job_hash = get_hash(payload['type'] + payload['url'])
    location = '/api/v1/job/' + job_hash
    assert response.headers['location'] == location

    response = client.get(location)
    assert response.status_code == 200  # OK
    assert response.is_json
    data = response.get_json()
    assert 'status' in data
    assert data['status'] in ['invalid URL error', 'not found', 'pending', 'done']


def test_get_textjob(client):
    payload = {
        'type': 'text',
        'url': 'http://www.lipsum.com'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code in (200, 201)

    job_hash = get_hash(payload['type'] + payload['url'])
    location = '/api/v1/job/' + job_hash + '/resources'
    response = client.get(location)
    assert response.status_code == 200  # OK
    assert response.is_json
    data = response.get_json()
    assert 'status' in data
    assert data['status'] in ['invalid URL error', 'not found', 'pending', 'done']
    assert 'data' in data
    assert isinstance(['data'], list)


def test_get_imagejob(client):
    payload = {
        'type': 'text',
        'url': 'http://www.lipsum.com'
    }
    response = client.post('/api/v1/job', json=payload)
    assert response.status_code in (200, 201)

    job_hash = get_hash(payload['type'] + payload['url'])
    location = '/api/v1/job/' + job_hash + '/resources'
    response = client.get(location)
    assert response.status_code == 200  # OK
    assert response.is_json
    data = response.get_json()
    assert 'status' in data
    assert data['status'] in ['invalid URL error', 'not found', 'pending', 'done']
    assert 'data' in data
    assert isinstance(['data'], list)
