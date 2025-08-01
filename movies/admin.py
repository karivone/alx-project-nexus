from django.contrib import admin
from .models import Movie, UserFavoriteMovie, UserMovieRating, UserWatchlist

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'tmdb_id', 'release_date', 'vote_average', 'popularity']
    list_filter = ['release_date', 'adult', 'original_language']
    search_fields = ['title', 'overview']
    readonly_fields = ['tmdb_id', 'created_at', 'updated_at']
    ordering = ['-popularity']

@admin.register(UserFavoriteMovie)
class UserFavoriteMovieAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'movie__title']
    raw_id_fields = ['user', 'movie']

@admin.register(UserMovieRating)
class UserMovieRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at', 'updated_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'movie__title']
    raw_id_fields = ['user', 'movie']

@admin.register(UserWatchlist)
class UserWatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'movie__title']
    raw_id_fields = ['user', 'movie']

# Register your models here.
