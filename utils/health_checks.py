"""Health check utilities for monitoring"""

import redis
from django.db import connection
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
import requests
from django.conf import settings

def database_health_check():
    """Check database connectivity"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return True, "Database connection OK"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def redis_health_check():
    """Check Redis connectivity"""
    try:
        cache.set('health_check', 'ok', 60)
        result = cache.get('health_check')
        if result == 'ok':
            return True, "Redis connection OK"
        else:
            return False, "Redis test failed"
    except Exception as e:
        return False, f"Redis error: {str(e)}"

def tmdb_api_health_check():
    """Check TMDb API connectivity"""
    try:
        url = f"{settings.TMDB_BASE_URL}/configuration"
        params = {'api_key': settings.TMDB_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return True, "TMDb API connection OK"
        else:
            return False, f"TMDb API returned {response.status_code}"
    except Exception as e:
        return False, f"TMDb API error: {str(e)}"

def health_check_view(request):
    """Comprehensive health check endpoint"""
    checks = {
        'database': database_health_check(),
        'redis': redis_health_check(),
        'tmdb_api': tmdb_api_health_check()
    }
    
    all_healthy = all(check[0] for check in checks.values())
    
    response_data = {
        'status': 'healthy' if all_healthy else 'unhealthy',
        'timestamp': timezone.now().isoformat(),
        'checks': {
            name: {
                'status': 'healthy' if check[0] else 'unhealthy',
                'message': check[1]
            }
            for name, check in checks.items()
        }
    }
    
    status_code = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    return JsonResponse(response_data, status=status_code)
