import os
import requests
from django.shortcuts import render

def movies(request):
    TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'dabc96b5a972e54425d4efd3010e893d')
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    movies = response.json().get('results', [])
    return render(request, 'movies.html', {'movies': movies})
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from .models import Movie, UserFavoriteMovie, UserMovieRating, UserWatchlist
from .serializers import (
    MovieSerializer, TMDbMovieSerializer, UserFavoriteMovieSerializer,
    UserMovieRatingSerializer, UserWatchlistSerializer
)
from .services import MovieService

logger = logging.getLogger(__name__)

class StandardResultsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('time_window', openapi.IN_QUERY, description="Time window (day/week)", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
    ],
    responses={200: TMDbMovieSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trending_movies(request):
    """Get trending movies from TMDb API"""
    time_window = request.GET.get('time_window', 'week')
    page = int(request.GET.get('page', 1))
    
    if time_window not in ['day', 'week']:
        return Response(
            {'error': 'time_window must be either "day" or "week"'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        data = MovieService.get_trending_movies(time_window, page)
        if data is None:
            return Response(
                {'error': 'Failed to fetch trending movies'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        return Response(data)
    except Exception as e:
        logger.error(f"Error fetching trending movies: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
    ],
    responses={200: TMDbMovieSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_movies(request):
    """Get popular movies from TMDb API"""
    page = int(request.GET.get('page', 1))
    
    try:
        data = MovieService.get_popular_movies(page)
        if data is None:
            return Response(
                {'error': 'Failed to fetch popular movies'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        return Response(data)
    except Exception as e:
        logger.error(f"Error fetching popular movies: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='get',
    responses={200: TMDbMovieSerializer()}
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def movie_details(request, movie_id):
    """Get detailed movie information"""
    try:
        data = MovieService.get_movie_details(movie_id)
        if data is None:
            return Response(
                {'error': 'Movie not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(data)
    except Exception as e:
        logger.error(f"Error fetching movie details for {movie_id}: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
    ],
    responses={200: TMDbMovieSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_movies(request):
    """Search movies by title"""
    query = request.GET.get('q')
    page = int(request.GET.get('page', 1))
    
    if not query:
        return Response(
            {'error': 'Search query (q) parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        data = MovieService.search_movies(query, page)
        if data is None:
            return Response(
                {'error': 'Failed to search movies'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        return Response(data)
    except Exception as e:
        logger.error(f"Error searching movies with query '{query}': {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
    ],
    responses={200: TMDbMovieSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def movie_recommendations(request, movie_id):
    """Get movie recommendations based on a specific movie"""
    page = int(request.GET.get('page', 1))
    
    try:
        data = MovieService.get_movie_recommendations(movie_id, page)
        if data is None:
            return Response(
                {'error': 'Failed to fetch recommendations'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        return Response(data)
    except Exception as e:
        logger.error(f"Error fetching recommendations for movie {movie_id}: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='get',
    responses={200: MovieSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def personalized_recommendations(request):
    """Get personalized movie recommendations for the authenticated user"""
    limit = int(request.GET.get('limit', 20))
    
    try:
        movies = MovieService.get_personalized_recommendations(request.user, limit)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error generating personalized recommendations for user {request.user.id}: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# User Favorites Views
class UserFavoriteMovieListCreateView(generics.ListCreateAPIView):
    """List user's favorite movies or add a new favorite"""
    serializer_class = UserFavoriteMovieSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        return UserFavoriteMovie.objects.filter(
            user=self.request.user
        ).select_related('movie').order_by('-created_at')
    
    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            return Response(
                {'error': 'Movie is already in favorites'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserFavoriteMovieDetailView(generics.DestroyAPIView):
    """Remove a movie from user's favorites"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserFavoriteMovie.objects.filter(user=self.request.user)
    
    def get_object(self):
        movie_id = self.kwargs.get('movie_id')
        return get_object_or_404(
            self.get_queryset(),
            movie__tmdb_id=movie_id
        )

# User Ratings Views
class UserMovieRatingListCreateView(generics.ListCreateAPIView):
    """List user's movie ratings or add/update a rating"""
    serializer_class = UserMovieRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        return UserMovieRating.objects.filter(
            user=self.request.user
        ).select_related('movie').order_by('-updated_at')
    
    def perform_create(self, serializer):
        # Check if rating already exists
        movie_id = serializer.validated_data['movie'].tmdb_id
        existing_rating = UserMovieRating.objects.filter(
            user=self.request.user,
            movie__tmdb_id=movie_id
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.rating = serializer.validated_data['rating']
            existing_rating.save()
            return existing_rating
        else:
            return serializer.save()

class UserMovieRatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific movie rating"""
    serializer_class = UserMovieRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserMovieRating.objects.filter(user=self.request.user)
    
    def get_object(self):
        movie_id = self.kwargs.get('movie_id')
        return get_object_or_404(
            self.get_queryset(),
            movie__tmdb_id=movie_id
        )

# User Watchlist Views
class UserWatchlistListCreateView(generics.ListCreateAPIView):
    """List user's watchlist or add a movie to watchlist"""
    serializer_class = UserWatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        return UserWatchlist.objects.filter(
            user=self.request.user
        ).select_related('movie').order_by('-created_at')
    
    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            return Response(
                {'error': 'Movie is already in watchlist'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserWatchlistDetailView(generics.DestroyAPIView):
    """Remove a movie from user's watchlist"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserWatchlist.objects.filter(user=self.request.user)
    
    def get_object(self):
        movie_id = self.kwargs.get('movie_id')
        return get_object_or_404(
            self.get_queryset(),
            movie__tmdb_id=movie_id
        ) 
# Create your views here.
