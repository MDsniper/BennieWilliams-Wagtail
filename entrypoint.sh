#!/usr/bin/env bash
set -e

echo "Starting entrypoint script..."

# Run database migrations unless explicitly disabled
if [ "$DJANGO_SKIP_MIGRATIONS" != "1" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if environment variables are set and user doesn't exist
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser if it doesn't exist..."
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

echo "Entrypoint script completed. Starting application..."

# Execute the main command
exec "$@"