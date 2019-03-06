#!/bin/sh

sleep 10

su -m mquser -c "celery worker -A src.celery -Q default -n default@%h --max-tasks-per-child=1"
