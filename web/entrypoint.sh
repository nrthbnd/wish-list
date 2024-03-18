##!/bin/sh
#
#if [ "$DATABASE" = "wish-list_db" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi
## shellcheck disable=SC1083
##uvicorn project.web.main:web --reload --host=0.0.0.0 --port="$PORT 8000"
#alembic revision --autogenerate -m "Initianal migration"
#alembic upgrade head
#uvicorn main:app --reload --host=0.0.0.0 --port=8000
#
#exec "$@"