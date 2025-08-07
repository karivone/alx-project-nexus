from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Movie(models.Model):
    """Movie model to store cached movie data"""
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    vote_average = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0.0)
    genre_ids = models.JSONField(default=list)
    adult = models.BooleanField(default=False)
    original_language = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'movies_movie'
        indexes = [
            models.Index(fields=['tmdb_id']),
            models.Index(fields=['popularity']),
            models.Index(fields=['vote_average']),
            models.Index(fields=['release_date']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.release_date.year if self.release_date else 'N/A'})"

class UserFavoriteMovie(models.Model):
    """Model to store user's favorite movies"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'movies_user_favorite'
        unique_together = ['user', 'movie']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class UserMovieRating(models.Model):
    """Model to store user movie ratings"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # 1-10 scale
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'movies_user_rating'
        unique_together = ['user', 'movie']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.user.username} rated {self.movie.title}: {self.rating}/10"

class UserWatchlist(models.Model):
    """Model to store user's watchlist"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'movies_user_watchlist'
        unique_together = ['user', 'movie']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - Watchlist: {self.movie.title}"
# Create your models here.
