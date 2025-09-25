# Multi-stage build for production
FROM python:3.12-slim-bookworm as builder

# Install build dependencies
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Final stage
FROM python:3.12-slim-bookworm

# Add user that will be used in the container
RUN useradd -m -u 1000 wagtail

# Install runtime dependencies
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libpq-dev \
    libjpeg62-turbo-dev \
    libwebp-dev \
    libmariadb-dev \
    curl \
    netcat-traditional \
 && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Install production server
RUN pip install gunicorn==23.0.0 whitenoise==6.5.0 dj-database-url==2.1.0 psycopg2-binary==2.9.9

# Use /app folder as a directory where the source code is stored
WORKDIR /app

# Copy the source code of the project into the container
COPY --chown=wagtail:wagtail . .

# Create necessary directories
RUN mkdir -p /app/media /app/static && \
    chown -R wagtail:wagtail /app

# Use user "wagtail" to run the build commands below and the server itself
USER wagtail

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=benniewilliams.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=4

# Collect static files
RUN python manage.py collectstatic --noinput --clear || true

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/')" || exit 1

# Port used by this container to serve HTTP
EXPOSE 8000

# Entrypoint script for database migration and server start
COPY --chown=wagtail:wagtail docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "benniewilliams.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--worker-class", "sync", "--worker-tmp-dir", "/dev/shm", "--access-logfile", "-", "--error-logfile", "-"]
