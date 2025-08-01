import requests
import logging
from django.conf import settings
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class TMDbClient:
    """Client for interacting with The Movie Database API"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.session = requests.Session()
        self.session.params = {'api_key': self.api_key}
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make a request to TMDb API with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDb API request failed: {e}")
            return None
    
    def get_trending_movies(self, time_window: str = 'week', page: int = 1) -> Optional[Dict]:
        """Get trending movies"""
        endpoint = f"trending/movie/{time_window}"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_popular_movies(self, page: int = 1) -> Optional[Dict]:
        """Get popular movies"""
        endpoint = "movie/popular"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Get detailed information about a specific movie"""
        endpoint = f"movie/{movie_id}"
        params = {'append_to_response': 'credits,videos,reviews'}
        return self._make_request(endpoint, params)
    
    def search_movies(self, query: str, page: int = 1) -> Optional[Dict]:
        """Search for movies"""
        endpoint = "search/movie"
        params = {'query': query, 'page': page}
        return self._make_request(endpoint, params)
    
    def get_movie_recommendations(self, movie_id: int, page: int = 1) -> Optional[Dict]:
        """Get movie recommendations based on a specific movie"""
        endpoint = f"movie/{movie_id}/recommendations"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_similar_movies(self, movie_id: int, page: int = 1) -> Optional[Dict]:
        """Get similar movies"""
        endpoint = f"movie/{movie_id}/similar"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def discover_movies(self, **kwargs) -> Optional[Dict]:
        """Discover movies with various filters"""
        endpoint = "discover/movie"
        return self._make_request(endpoint, kwargs)

# Global instance
tmdb_client = TMDbClient()
