from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from movies.models import Movie, UserFavoriteMovie

User = get_user_model()

class MovieViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            tmdb_id=550,
            title='Fight Club',
            vote_average=8.8
        )
    
    def test_trending_movies_public_access(self):
        """Test that trending movies endpoint is publicly accessible"""
        with patch('movies.services.MovieService.get_trending_movies') as mock_service:
            mock_service.return_value = {'results': []}
            
            url = reverse('trending-movies')
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_personalized_recommendations_requires_auth(self):
        """Test that personalized recommendations require authentication"""
        url = reverse('personalized-recommendations')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_favorite_movie(self):
        """Test adding a movie to favorites"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('user-favorites')
        data = {'movie_id': self.movie.tmdb_id}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            UserFavoriteMovie.objects.filter(
                user=self.user, 
                movie=self.movie
            ).exists()
        )
    
    def test_remove_favorite_movie(self):
        """Test removing a movie from favorites"""
        self.client.force_authenticate(user=self.user)
        
        # First add to favorites
        UserFavoriteMovie.objects.create(user=self.user, movie=self.movie)
        
        # Then remove
        url = reverse('user-favorite-detail', kwargs={'movie_id': self.movie.tmdb_id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            UserFavoriteMovie.objects.filter(
                user=self.user, 
                movie=self.movie
            ).exists()
        )
