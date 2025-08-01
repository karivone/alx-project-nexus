import logging
from typing import Dict, List, Optional, Tuple
from django.core.paginator import Paginator
from django.db import transaction
from .models import Movie, UserFavoriteMovie, UserMovieRating
from utils.tmdb_client import tmdb_client
from utils.redis_client import (
    redis_client, 
    generate_trending_key, 
    generate_popular_key,
    generate_movie_details_key,
    generate_recommendations_key,
    generate_search_key
)

logger = logging.getLogger(__name__)

class MovieService:
    """Service class for movie-related operations"""
    
    @staticmethod
    def get_or_create_movie_from_tmdb_data(tmdb_data: Dict) -> Tuple[Movie, bool]:
        """Create or update movie from TMDb data"""
        try:
            movie, created = Movie.objects.update_or_create(
                tmdb_id=tmdb_data['id'],
                defaults={
                    'title': tmdb_data.get('title', ''),
                    'overview': tmdb_data.get('overview', ''),
                    'release_date': tmdb_data.get('release_date'),
                    'poster_path': tmdb_data.get('poster_path', ''),
                    'backdrop_path': tmdb_data.get('backdrop_path', ''),
                    'vote_average': tmdb_data.get('vote_average', 0.0),
                    'vote_count': tmdb_data.get('vote_count', 0),
                    'popularity': tmdb_data.get('popularity', 0.0),
                    'genre_ids': tmdb_data.get('genre_ids', []),
                    'adult': tmdb_data.get('adult', False),
                    'original_language': tmdb_data.get('original_language', ''),
                }
            )
            return movie, created
        except Exception as e:
            logger.error(f"Error creating/updating movie {tmdb_data.get('id')}: {e}")
            raise
    
    @staticmethod
    def get_trending_movies(time_window: str = 'week', page: int = 1, use_cache: bool = True) -> Optional[Dict]:
        """Get trending movies with caching"""
        cache_key = generate_trending_key(time_window, page)
        
        # Try cache first if enabled
        if use_cache:
            cached_data = redis_client.get_cache(cache_key)
            if cached_data:
                logger.info(f"Cache hit for trending movies: {cache_key}")
                return cached_data
        
        # Fetch from TMDb API
        tmdb_data = tmdb_client.get_trending_movies(time_window, page)
        if not tmdb_data:
            return None
        
        # Process and cache the data
        processed_data = MovieService._process_movie_list_data(tmdb_data)
        
        if use_cache and processed_data:
            redis_client.set_cache(cache_key, processed_data, timeout=1800)  # 30 minutes
            logger.info(f"Cached trending movies: {cache_key}")
        
        return processed_data
    
    @staticmethod
    def get_popular_movies(page: int = 1, use_cache: bool = True) -> Optional[Dict]:
        """Get popular movies with caching"""
        cache_key = generate_popular_key(page)
        
        if use_cache:
            cached_data = redis_client.get_cache(cache_key)
            if cached_data:
                logger.info(f"Cache hit for popular movies: {cache_key}")
                return cached_data
        
        tmdb_data = tmdb_client.get_popular_movies(page)
        if not tmdb_data:
            return None
        
        processed_data = MovieService._process_movie_list_data(tmdb_data)
        
        if use_cache and processed_data:
            redis_client.set_cache(cache_key, processed_data, timeout=1800)
            logger.info(f"Cached popular movies: {cache_key}")
        
        return processed_data
    
    @staticmethod
    def get_movie_details(movie_id: int, use_cache: bool = True) -> Optional[Dict]:
        """Get detailed movie information with caching"""
        cache_key = generate_movie_details_key(movie_id)
        
        if use_cache:
            cached_data = redis_client.get_cache(cache_key)
            if cached_data:
                logger.info(f"Cache hit for movie details: {cache_key}")
                return cached_data
        
        tmdb_data = tmdb_client.get_movie_details(movie_id)
        if not tmdb_data:
            return None
        
        # Store/update movie in database
        try:
            MovieService.get_or_create_movie_from_tmdb_data(tmdb_data)
        except Exception as e:
            logger.error(f"Failed to store movie {movie_id}: {e}")
        
        # Add full image URLs
        processed_data = MovieService._add_image_urls(tmdb_data)
        
        if use_cache and processed_data:
            redis_client.set_cache(cache_key, processed_data, timeout=3600)  # 1 hour
            logger.info(f"Cached movie details: {cache_key}")
        
        return processed_data
    
    @staticmethod
    def search_movies(query: str, page: int = 1, use_cache: bool = True) -> Optional[Dict]:
        """Search movies with caching"""
        cache_key = generate_search_key(query, page)
        
        if use_cache:
            cached_data = redis_client.get_cache(cache_key)
            if cached_data:
                logger.info(f"Cache hit for movie search: {cache_key}")
                return cached_data
        
        tmdb_data = tmdb_client.search_movies(query, page)
        if not tmdb_data:
            return None
        
        processed_data = MovieService._process_movie_list_data(tmdb_data)
        
        if use_cache and processed_data:
            redis_client.set_cache(cache_key, processed_data, timeout=900)  # 15 minutes
            logger.info(f"Cached movie search: {cache_key}")
        
        return processed_data
    
    @staticmethod
    def get_movie_recommendations(movie_id: int, page: int = 1, use_cache: bool = True) -> Optional[Dict]:
        """Get movie recommendations with caching"""
        cache_key = generate_recommendations_key(movie_id, page)
        
        if use_cache:
            cached_data = redis_client.get_cache(cache_key)
            if cached_data:
                logger.info(f"Cache hit for recommendations: {cache_key}")
                return cached_data
        
        tmdb_data = tmdb_client.get_movie_recommendations(movie_id, page)
        if not tmdb_data:
            return None
        
        processed_data = MovieService._process_movie_list_data(tmdb_data)
        
        if use_cache and processed_data:
            redis_client.set_cache(cache_key, processed_data, timeout=2700)  # 45 minutes
            logger.info(f"Cached recommendations: {cache_key}")
        
        return processed_data
    
    @staticmethod
    def get_personalized_recommendations(user, limit: int = 20) -> List[Movie]:
        """Get personalized recommendations based on user preferences"""
        try:
            # Get user's favorite genres from their rated/favorite movies
            user_ratings = UserMovieRating.objects.filter(user=user, rating__gte=7)
            favorite_movies = UserFavoriteMovie.objects.filter(user=user)
            
            # Extract preferred genres
            preferred_genres = set()
            for rating in user_ratings:
                preferred_genres.update(rating.movie.genre_ids)
            for favorite in favorite_movies:
                preferred_genres.update(favorite.movie.genre_ids)
            
            # Get movies the user hasn't interacted with
            excluded_movie_ids = set()
            excluded_movie_ids.update(
                user_ratings.values_list('movie__tmdb_id', flat=True)
            )
            excluded_movie_ids.update(
                favorite_movies.values_list('movie__tmdb_id', flat=True)
            )
            
            # Find movies with similar genres, high ratings, and popularity
            recommended_movies = Movie.objects.exclude(
                tmdb_id__in=excluded_movie_ids
            ).filter(
                vote_average__gte=6.0,
                vote_count__gte=100
            ).order_by('-popularity', '-vote_average')[:limit]
            
            return list(recommended_movies)
            
        except Exception as e:
            logger.error(f"Error generating personalized recommendations for user {user.id}: {e}")
            return []
    
    @staticmethod
    def _process_movie_list_data(tmdb_data: Dict) -> Dict:
        """Process TMDb movie list data and add image URLs"""
        if not tmdb_data or 'results' not in tmdb_data:
            return tmdb_data
        
        processed_results = []
        for movie in tmdb_data['results']:
            processed_movie = MovieService._add_image_urls(movie)
            processed_results.append(processed_movie)
            
            # Store movie in database for future use
            try:
                MovieService.get_or_create_movie_from_tmdb_data(movie)
            except Exception as e:
                logger.error(f"Failed to store movie {movie.get('id')}: {e}")
        
        tmdb_data['results'] = processed_results
        return tmdb_data
    
    @staticmethod
    def _add_image_urls(movie_data: Dict) -> Dict:
        """Add full image URLs to movie data"""
        movie_copy = movie_data.copy()
        
        if movie_copy.get('poster_path'):
            movie_copy['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie_copy['poster_path']}"
        
        if movie_copy.get('backdrop_path'):
            movie_copy['backdrop_url'] = f"https://image.tmdb.org/t/p/w1280{movie_copy['backdrop_path']}"
        
        return movie_copy
