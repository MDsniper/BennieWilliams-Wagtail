"""
Health check views for monitoring deployment status
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Simple health check endpoint for load balancers and monitoring
    Returns JSON with system status
    """
    try:
        # Check database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"

    # Check cache connectivity (Redis or database cache)
    try:
        cache.set('health_check', 'ok', 10)
        cache_result = cache.get('health_check')
        cache_status = "healthy" if cache_result == 'ok' else "unhealthy"
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        cache_status = "unhealthy"

    overall_status = "healthy" if (db_status == "healthy" and cache_status == "healthy") else "unhealthy"

    response_data = {
        "status": overall_status,
        "database": db_status,
        "cache": cache_status,
        "application": "benniewilliams-wagtail"
    }

    status_code = 200 if overall_status == "healthy" else 503
    return JsonResponse(response_data, status=status_code)


@csrf_exempt
@require_http_methods(["GET"])
def readiness_check(request):
    """
    Readiness check for deployment orchestration
    More comprehensive than health check
    """
    checks = {}

    # Database check
    try:
        from django.contrib.auth.models import User
        User.objects.exists()  # Test actual query
        checks["database"] = "ready"
    except Exception as e:
        logger.error(f"Database readiness failed: {e}")
        checks["database"] = "not_ready"

    # Static files check
    try:
        from django.conf import settings
        import os
        static_dir_exists = os.path.exists(settings.STATIC_ROOT) if settings.STATIC_ROOT else False
        checks["static_files"] = "ready" if static_dir_exists else "not_ready"
    except Exception as e:
        logger.error(f"Static files check failed: {e}")
        checks["static_files"] = "not_ready"

    # Cache check
    try:
        cache.set('readiness_check', 'ready', 10)
        cache_result = cache.get('readiness_check')
        checks["cache"] = "ready" if cache_result == 'ready' else "not_ready"
    except Exception as e:
        logger.error(f"Cache readiness failed: {e}")
        checks["cache"] = "not_ready"

    all_ready = all(status == "ready" for status in checks.values())
    overall_status = "ready" if all_ready else "not_ready"

    response_data = {
        "status": overall_status,
        "checks": checks,
        "application": "benniewilliams-wagtail"
    }

    status_code = 200 if all_ready else 503
    return JsonResponse(response_data, status=status_code)