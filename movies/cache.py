from django.core.cache import cache
from django.conf import settings
import hashlib
import json
from typing import Any, Optional

class CacheManager:
    """Enhanced cache manager with TTL and key management"""
    
    DEFAULT_TIMEOUT = 300  # 5 minutes
    
    @staticmethod
    def generate_key(*args, **kwargs) -> str:
        """Generate a cache key from arguments"""
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    @staticmethod
    def set(key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """Set cache with optional timeout"""
        timeout = timeout or CacheManager.DEFAULT_TIMEOUT
        try:
            cache.set(key, value, timeout)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get value from cache"""
        try:
            return cache.get(key, default)
        except Exception:
            return default
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete key from cache"""
        try:
            cache.delete(key)
            return True
        except Exception:
            return False
    
    @staticmethod
    def clear_pattern(pattern: str) -> bool:
        """Clear cache keys matching pattern (Redis specific)"""
        try:
            # This works with django-redis
            cache.delete_pattern(pattern)
            return True
        except (AttributeError, Exception):
            return False
