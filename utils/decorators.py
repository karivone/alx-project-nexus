"""Custom decorators for the movie recommendation app"""

import functools
import time
import logging
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from .exceptions import RateLimitException

logger = logging.getLogger(__name__)

def cache_result(timeout=300, key_func=None):
    """Decorator to cache function results"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                logger.info(f"Cache hit for {cache_key}")
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            logger.info(f"Cached result for {cache_key}")
            
            return result
        return wrapper
    return decorator

def rate_limit(max_requests=10, window=60):
    """Decorator to rate limit function calls"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            # Get client identifier
            client_id = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
            cache_key = f"rate_limit:{func.__name__}:{client_id}"
            
            # Get current count
            current_count = cache.get(cache_key, 0)
            
            if current_count >= max_requests:
                raise RateLimitException("Rate limit exceeded", retry_after=window)
            
            # Increment count
            cache.set(cache_key, current_count + 1, window)
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def retry_on_failure(max_retries=3, delay=1, backoff=2):
    """Decorator to retry function on failure with exponential backoff"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise
                    
                    logger.warning(f"Function {func.__name__} failed (attempt {retries}/{max_retries}): {e}")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            return None
        return wrapper
    return decorator

def log_execution_time(func):
    """Decorator to log function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.3f} seconds")
        return result
    return wrapper
