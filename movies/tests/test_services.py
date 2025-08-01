from django.test import TestCase
from unittest.mock import Mock, patch
from movies.services import MovieService
from movies.models import Movie

class MovieServiceTest(TestCase):
    
    @patch('movies.services.tmdb_client')
    @patch('movies.services.redis_client')
    def test_get_trending_movies_with_cache(self, mock_redis, mock_tmdb):
        """Test getting trending movies with cache hit"""
        # Setup cache hit
        cached_data = {'results': [{'id': 1, 'title': 'Test Movie'}]}
        mock_redis.get_cache.return_value = cached_data
        
        result = MovieService.get_trending_movies()
        
        self.assertEqual(result, cached_data)
        mock_redis.get_cache.assert_called_once()
        mock_tmdb.get_trending_movies.assert_not_called()
    
    @patch('movies.services.tmdb_client')
    @patch('movies.services.redis_client')
    def test_get_trending_movies_cache_miss(self, mock_redis, mock_tmdb):
        """Test getting trending movies with cache miss"""
        # Setup cache miss
        mock_redis.get_cache.return_value = None
        tmdb_data = {
            'results': [{
                'id': 1,
                'title': 'Test Movie',
                'overview': 'Test overview',
                'release_date': '2023-01-01',
                'vote_average': 7.5,
                'vote_count': 1000,
                'popularity': 50.0,
                'genre_ids': [28],
                'adult': False,
                'original_language': 'en',
                'poster_path': '/test.jpg',
                'backdrop_path': '/test_bg.jpg'
            }]
        }
        mock_tmdb.get_trending_movies.return_value = tmdb_data
        
        result = MovieService.get_trending_movies()
        
        mock_tmdb.get_trending_movies.assert_called_once()
        mock_redis.set_cache.assert_called_once()
        self.assertIsNotNone(result)
    
    def test_get_or_create_movie_from_tmdb_data(self):
        """Test creating movie from TMDb data"""
        tmdb_data = {
            'id': 550,
            'title': 'Fight Club',
            'overview': 'Test overview',
            'release_date': '1999-10-15',
            'vote_average': 8.8,
            'vote_count': 26000,
            'popularity': 61.416,
            'genre_ids': [18, 53],
            'adult': False,
            'original_language': 'en',
            'poster_path': '/test.jpg',
            'backdrop_path': '/test_bg.jpg'
        }
        
        movie, created = MovieService.get_or_create_movie_from_tmdb_data(tmdb_data)
        
        self.assertTrue(created)
        self.assertEqual(movie.tmdb_id, 550)
        self.assertEqual(movie.title, 'Fight Club'
