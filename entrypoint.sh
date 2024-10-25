#!/bin/sh

if [ "$DATABASE" = "education" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python education/manage.py flush --no-input
python education/manage.py migrate

exec "$@"