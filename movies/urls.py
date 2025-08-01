from django.urls import path
from . import views

urlpatterns = [
    # Public movie endpoints
    path('trending/', views.trending_movies, name='trending-movies'),
    path('popular/', views.popular_movies, name='popular-movies'),
    path('search/', views.search_movies, name='search-movies'),
    path('<int:movie_id>/', views.movie_details, name='movie-details'),
    path('<int:movie_id>/recommendations/', views.movie_recommendations, name='movie-recommendations'),
    
    # Personalized recommendations (requires authentication)
    path('recommendations/personalized/', views.personalized_recommendations, name='personalized-recommendations'),
    
    # User favorites
    path('favorites/', views.UserFavoriteMovieListCreateView.as_view(), name='user-favorites'),
    path('favorites/<int:movie_id>/', views.UserFavoriteMovieDetailView.as_view(), name='user-favorite-detail'),
    
    # User ratings
    path('ratings/', views.UserMovieRatingListCreateView.as_view(), name='user-ratings'),
    path('ratings/<int:movie_id>/', views.UserMovieRatingDetailView.as_view(), name='user-rating-detail'),
    
    # User watchlist
    path('watchlist/', views.UserWatchlistListCreateView.as_view(), name='user-watchlist'),
    path('watchlist/<int:movie_id>/', views.UserWatchlistDetailView.as_view(), name='user-watchlist-detail'),
]
