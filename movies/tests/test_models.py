from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from datetime import date
from movies.models import Movie, UserFavoriteMovie, UserMovieRating, UserWatchlist

User = get_user_model()

class MovieModelTest(TestCase):
    def setUp(self):
        self.movie_data = {
            'tmdb_id': 550,
            'title': 'Fight Club',
            'overview': 'A ticking-time-bomb insomniac...',
            'release_date': date(1999, 10, 15),
            'vote_average': 8.8,
            'vote_count': 26000,
            'popularity': 61.416,
            'genre_ids': [18, 53],
        }
    
    def test_movie_creation(self):
        """Test creating a movie instance"""
        movie = Movie.objects.create(**self.movie_data)
        self.assertEqual(movie.title, 'Fight Club')
        self.assertEqual(movie.tmdb_id, 550)
        self.assertEqual(str(movie), 'Fight Club (1999)')
    
    def test_movie_unique_tmdb_id(self):
        """Test that tmdb_id is unique"""
        Movie.objects.create(**self.movie_data)
        with self.assertRaises(IntegrityError):
            Movie.objects.create(**self.movie_data)

class UserFavoriteMovieTest(TestCase):
    def setUp(self):
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
    
    def test_favorite_creation(self):
        """Test creating a favorite movie"""
        favorite = UserFavoriteMovie.objects.create(
            user=self.user,
            movie=self.movie
        )
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.movie, self.movie)
    
    def test_unique_user_movie_favorite(self):
        """Test that user can't favorite same movie twice"""
        UserFavoriteMovie.objects.create(user=self.user, movie=self.movie)
        with self.assertRaises(IntegrityError):
            UserFavoriteMovie.objects.create(user=self.user, movie=self.movie)

class UserMovieRatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            tmdb_id=550,
            title='Fight Club'
        )
    
    def test_rating_creation(self):
        """Test creating a movie rating"""
        rating = UserMovieRating.objects.create(
            user=self.user,
            movie=self.movie,
            rating=9
        )
        self.assertEqual(rating.rating, 9)
        self.assertEqual(str(rating), 'testuser rated Fight Club: 9/10')
    
    def test_rating_validation(self):
        """Test rating is within valid range"""
        # Valid rating
        rating = UserMovieRating.objects.create(
            user=self.user,
            movie=self.movie,
            rating=8
        )
        self.assertEqual(rating.rating, 8)
