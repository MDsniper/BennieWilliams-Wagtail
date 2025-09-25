#!/bin/bash
set -e

echo "Starting Wagtail application..."

# Wait for database to be ready
if [ "$DATABASE_URL" ]; then
    echo "Waiting for database..."
    while ! nc -z ${DB_HOST:-db} ${DB_PORT:-5432}; do
        sleep 1
    done
    echo "Database is ready!"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create cache table if using database cache
python manage.py createcachetable 2>/dev/null || true

# Create superuser if doesn't exist
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created.');
else:
    print('Superuser already exists.');
"
fi

# Collect static files if needed
if [ "$DJANGO_COLLECT_STATIC" = "true" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Start server
echo "Starting Gunicorn..."
exec "$@"