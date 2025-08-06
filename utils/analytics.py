"""Analytics and monitoring utilities"""

import logging
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Count, Avg
from movies.models import Movie, UserFavoriteMovie, UserMovieRating
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for application analytics and monitoring"""
    
    @staticmethod
    def get_api_stats():
        """Get API usage statistics"""
        stats = {
            'total_users': User.objects.count(),
            'total_movies': Movie.objects.count(),
            'total_favorites': UserFavoriteMovie.objects.count(),
            'total_ratings': UserMovieRating.objects.count(),
            'average_rating': UserMovieRating.objects.aggregate(
                avg_rating=Avg('rating')
            )['avg_rating'] or 0,
        }
        
        # Cache stats for 5 minutes
        cache.set('api_stats', stats, 300)
        return stats
    
    @staticmethod
    def get_popular_movies_stats(limit=10):
        """Get most popular movies by user interactions"""
        popular_by_favorites = UserFavoriteMovie.objects.values(
            'movie__title', 'movie__tmdb_id'
        ).annotate(
            favorite_count=Count('id')
        ).order_by('-favorite_count')[:limit]
        
        popular_by_ratings = UserMovieRating.objects.values(
            'movie__title', 'movie__tmdb_id'
        ).annotate(
            rating_count=Count('id'),
            avg_rating=Avg('rating')
        ).order_by('-rating_count')[:limit]
        
        return {
            'most_favorited': list(popular_by_favorites),
            'most_rated': list(popular_by_ratings)
        }
    
    @staticmethod
    def get_user_engagement_stats():
        """Get user engagement statistics"""
        users_with_favorites = User.objects.filter(
            favorite_movies__isnull=False
        ).distinct().count()
        
        users_with_ratings = User.objects.filter(
            movie_ratings__isnull=False
        ).distinct().count()
        
        active_users = User.objects.filter(
            models.Q(favorite_movies__isnull=False) | 
            models.Q(movie_ratings__isnull=False)
        ).distinct().count()
        
        return {
            'users_with_favorites': users_with_favorites,
            'users_with_ratings': users_with_ratings,
            'active_users': active_users,
            'engagement_rate': (active_users / max(User.objects.count(), 1)) * 100
        }
    
    @staticmethod
    def log_api_call(endpoint, method, response_time, status_code, user_id=None):
        """Log API call for analytics"""
        log_data = {
            'endpoint': endpoint,
            'method': method,
            'response_time': response_time,
            'status_code': status_code,
            'user_id': user_id,
            'timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"API_CALL: {log_data}")
        
        # Store in cache for real-time monitoring
        cache_key = f"api_calls:{timezone.now().strftime('%Y-%m-%d-%H')}"
        current_calls = cache.get(cache_key, [])
        current_calls.append(log_data)
        cache.set(cache_key, current_calls, 3600)  # 1 hour
