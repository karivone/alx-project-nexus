import redis
import json
import logging
from django.conf import settings
from typing import Any, Optional
from django.core.cache import cache

logger = logging.getLogger(__name__)

class RedisClient:
    """Redis client for caching movie data"""
    
    def __init__(self):
        self.redis_url = getattr(settings, 'REDIS_URL', 'redis://redis:6379/0')
        try:
            self.client = redis.from_url(self.redis_url, decode_responses=True)
            self.client.ping()
        except redis.ConnectionError as e:
            logger.error(f"Redis connection failed: {e}")
            self.client = None
    
    def set_cache(self, key: str, value: Any, timeout: int = 300) -> bool:
        """Set cache with JSON serialization"""
        if not self.client:
            return False
        
        try:
            serialized_value = json.dumps(value)
            return self.client.setex(key, timeout, serialized_value)
        except (json.JSONEncodeError, redis.RedisError) as e:
            logger.error(f"Cache set failed for key {key}: {e}")
            return False
    
    def get_cache(self, key: str) -> Optional[Any]:
        """Get cache with JSON deserialization"""
        if not self.client:
            return None
        
        try:
            cached_value = self.client.get(key)
            if cached_value:
                return json.loads(cached_value)
            return None
        except (json.JSONDecodeError, redis.RedisError) as e:
            logger.error(f"Cache get failed for key {key}: {e}")
            return None
    
    def delete_cache(self, key: str) -> bool:
        """Delete cache entry"""
        if not self.client:
            return False
        
        try:
            return bool(self.client.delete(key))
        except redis.RedisError as e:
            logger.error(f"Cache delete failed for key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.client:
            return False
        
        try:
            return bool(self.client.exists(key))
        except redis.RedisError as e:
            logger.error(f"Cache exists check failed for key {key}: {e}")
            return False

# Global instance
redis_client = RedisClient()

# Cache key generators
def generate_trending_key(time_window: str = 'week', page: int = 1) -> str:
    return f"trending_movies:{time_window}:page:{page}"

def generate_popular_key(page: int = 1) -> str:
    return f"popular_movies:page:{page}"

def generate_movie_details_key(movie_id: int) -> str:
    return f"movie_details:{movie_id}"

def generate_recommendations_key(movie_id: int, page: int = 1) -> str:
    return f"recommendations:{movie_id}:page:{page}"

def generate_search_key(query: str, page: int = 1) -> str:
    return f"search:{query}:page:{page}"
