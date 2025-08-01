from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from movies.services import MovieService
from movies.models import UserMovieRating, UserFavoriteMovie
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate and cache personalized recommendations for all users'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='Generate recommendations for specific user ID'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Number of recommendations per user (default: 50)'
        )
    
    def handle(self, *args, **options):
        user_id = options.get('user_id')
        limit = options['limit']
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                users = [user]
                self.stdout.write(f'Generating recommendations for user: {user.username}')
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with ID {user_id} not found')
                )
                return
        else:
            # Get users who have ratings or favorites
            users = User.objects.filter(
                models.Q(movie_ratings__isnull=False) | 
                models.Q(favorite_movies__isnull=False)
            ).distinct()
            self.stdout.write(f'Generating recommendations for {users.count()} users')
        
        success_count = 0
        error_count = 0
        
        for user in users:
            try:
                recommendations = MovieService.get_personalized_recommendations(user, limit)
                
                if recommendations:
                    # Cache the recommendations
                    from utils.redis_client import redis_client
                    cache_key = f"personalized_recommendations:{user.id}"
                    recommendation_data = [
                        {
                            'id': movie.tmdb_id,
                            'title': movie.title,
                            'vote_average': float(movie.vote_average),
                            'popularity': movie.popularity
                        }
                        for movie in recommendations
                    ]
                    redis_client.set_cache(cache_key, recommendation_data, timeout=86400)  # 24 hours
                    
                    success_count += 1
                    self.stdout.write(f'  ✓ {user.username}: {len(recommendations)} recommendations')
                else:
                    self.stdout.write(f'  - {user.username}: No recommendations generated')
                    
            except Exception as e:
                error_count += 1
                logger.error(f'Error generating recommendations for user {user.id}: {e}')
                self.stdout.write(
                    self.style.ERROR(f'  ✗ {user.username}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Completed. Success: {success_count}, Errors: {error_count}'
            )
        )
