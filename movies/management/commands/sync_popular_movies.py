from django.core.management.base import BaseCommand
from django.utils import timezone
from movies.services import MovieService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync popular movies from TMDb API to local database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            default=5,
            help='Number of pages to sync (default: 5)'
        )
        parser.add_argument(
            '--clear-cache',
            action='store_true',
            help='Clear cache after sync'
        )
    
    def handle(self, *args, **options):
        pages = options['pages']
        clear_cache = options['clear_cache']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting sync of {pages} pages of popular movies...')
        )
        
        synced_count = 0
        errors = 0
        
        for page in range(1, pages + 1):
            try:
                self.stdout.write(f'Syncing page {page}...')
                
                # Get data without cache to ensure fresh data
                data = MovieService.get_popular_movies(page, use_cache=False)
                
                if data and 'results' in data:
                    for movie_data in data['results']:
                        try:
                            movie, created = MovieService.get_or_create_movie_from_tmdb_data(movie_data)
                            if created:
                                synced_count += 1
                                self.stdout.write(f'  Added: {movie.title}')
                            else:
                                self.stdout.write(f'  Updated: {movie.title}')
                        except Exception as e:
                            errors += 1
                            logger.error(f'Error syncing movie {movie_data.get("id")}: {e}')
                else:
                    self.stdout.write(
                        self.style.WARNING(f'No data received for page {page}')
                    )
                    
            except Exception as e:
                errors += 1
                logger.error(f'Error syncing page {page}: {e}')
                self.stdout.write(
                    self.style.ERROR(f'Error syncing page {page}: {e}')
                )
        
        if clear_cache:
            from utils.redis_client import redis_client
            redis_client.client.flushdb()
            self.stdout.write(self.style.SUCCESS('Cache cleared.'))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Sync completed. Added/Updated: {synced_count} movies. Errors: {errors}'
            )
        )
