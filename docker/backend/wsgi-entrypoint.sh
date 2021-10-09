#!/usr/bin/env sh

ls -al /app
until cd /app
do
    echo "Waiting for server volume..."
done

until ./manage.py migrate
do
    echo "Waiting for postgres ready..."
    sleep 2
done

./manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'Aa123456') if not User.objects.filter(email='admin@example.com', is_superuser=True).exists() else print('Db already has an admin user')"

./manage.py collectstatic --noinput

./manage.py compilemessages

gunicorn mobility.wsgi:application --bind 0.0.0.0:8000
