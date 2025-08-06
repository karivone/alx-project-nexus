"""Custom exception classes for the movie recommendation app"""

class MovieRecommendationException(Exception):
    """Base exception for movie recommendation app"""
    pass

class TMDbAPIException(MovieRecommendationException):
    """Exception for TMDb API related errors"""
    def __init__(self, message, status_code=None, response_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class CacheException(MovieRecommendationException):
    """Exception for cache related errors"""
    pass

class RecommendationException(MovieRecommendationException):
    """Exception for recommendation generation errors"""
    pass

class RateLimitException(MovieRecommendationException):
    """Exception for rate limiting errors"""
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after
