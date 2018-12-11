#!/usr/bin/env bash

docker-compose exec flask-app sh -c 'cd tests && pytest -v'
