import urllib.parse
import urllib.request
from os import abort

from flask import Blueprint, request, abort, jsonify, make_response, url_for

from .filesapi import files_api_wrapper
from .redisapi import RedisApi

rest_api = Blueprint("rest_api", __name__)


@rest_api.route('/job', methods=['POST'])
def add_job():
    """Create new download job"""

    # validation
    if not request.json:
        abort(400, 'Request should contain "type" of [text|images] and "url".')
    payload = request.json
    if 'type' not in payload or 'url' not in payload:
        abort(400, 'Request should contain "type" of [text|images] and "url".')
    if payload['type'] not in ['text', 'images'] or len(payload['url']) == 0:
        abort(400, 'Request should contain "type" of [text|images] and "url".')

    job_type = payload['type']
    job_url = payload['url']

    try:
        urllib.request.Request(job_url)
    except ValueError as e:
        abort(400, 'Provided url is invalid.')

    # adding job
    redis_api = RedisApi()
    job_hash, status = redis_api.add_job(job_type=job_type, job_url=job_url)

    location = url_for('.get_job_info', job_hash=job_hash, _external=False)
    response = make_response('', 201 if status == 0 else 200)
    response.autocorrect_location_header = False
    response.headers['Location'] = location
    return response


@rest_api.route('/job/<string(length=32):job_hash>', methods=['GET'])
def get_job_info(job_hash):
    """Get job status"""

    redis_api = RedisApi()
    status = redis_api.get_status(job_hash=job_hash)

    response_dict = {'status': status}
    return jsonify(response_dict), 200


@rest_api.route('/job/<string(length=32):job_hash>/resources', methods=['GET'])
def get_job_resources(job_hash):
    """Get job resources"""

    redis_api = RedisApi()
    status = redis_api.get_status(job_hash=job_hash)

    data = []
    if status == 'done':
        data.extend(files_api_wrapper(job_hash=job_hash))

    response_dict = {'status': status, 'data': data}
    return jsonify(response_dict), 200
