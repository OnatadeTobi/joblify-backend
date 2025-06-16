#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py shell < scripts/createsuperuser.py

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
PORT=${PORT:-8000}
exec gunicorn JoblifyBackend.wsgi:application --bind 0.0.0.0:$PORT


#works perfectly with render, just commented it out to test railway
exec gunicorn JoblifyBackend.wsgi:application --bind 0.0.0.0:8000




# #!/bin/sh

# echo "Running migrations..."
# python manage.py migrate

# echo "Creating superuser if it doesn't exist..."
# python manage.py shell -c "
# from django.contrib.auth import get_user_model
# User = get_user_model()
# username = '${DJANGO_SUPERUSER_USERNAME:-admin}'
# email = '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}'
# password = '${DJANGO_SUPERUSER_PASSWORD:-adminpassword}'
# if not User.objects.filter(username=username).exists():
#     User.objects.create_superuser(username=username, email=email, password=password)
# "

# echo "Collecting static files..."
# python manage.py collectstatic --noinput


# echo "Starting server..."
# exec gunicorn JoblifyBackend.wsgi:application --bind 0.0.0.0:8000
