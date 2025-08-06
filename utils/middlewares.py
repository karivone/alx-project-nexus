"""Custom middleware for the movie recommendation app"""

import time
import logging
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from rest_framework import status

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware to log API requests and responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.path}")
        
        response = self.get_response(request)
        
        # Log response time
        duration = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {duration:.3f}s")
        
        return response

class RateLimitMiddleware:
    """Simple rate limiting middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = getattr(settings, 'API_RATE_LIMIT', 100)  # requests per minute
        self.window = 60  # 1 minute window
    
    def __call__(self, request):
        # Skip rate limiting for admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Get client IP
        client_ip = self.get_client_ip(request)
        cache_key = f"rate_limit:{client_ip}"
        
        # Get current request count
        current_requests = cache.get(cache_key, 0)
        
        if current_requests >= self.rate_limit:
            return JsonResponse(
                {'error': 'Rate limit exceeded. Try again later.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Increment counter
        cache.set(cache_key, current_requests + 1, self.window)
        
        response = self.get_response(request)
        
        # Add rate limit headers
        response['X-RateLimit-Limit'] = str(self.rate_limit)
        response['X-RateLimit-Remaining'] = str(max(0, self.rate_limit - current_requests - 1))
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class APIVersioningMiddleware:
    """Middleware to handle API versioning"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add API version to request
        api_version = request.headers.get('API-Version', 'v1')
        request.api_version = api_version
        
        response = self.get_response(request)
        
        # Add version header to response
        response['API-Version'] = api_version

        return response
