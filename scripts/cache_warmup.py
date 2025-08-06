#!/usr/bin/env python
"""Cache warmup script to pre-populate frequently accessed data"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_backend.settings')
django.setup()

from movies.services import MovieService
from django.contrib.auth import get_user_model
import time

User = get_user_model()

def warmup_trending_movies():
    """Warmup trending movies cache"""
    print("Warming up trending movies cache...")
    for time_window in ['day', 'week']:
        for page in range(1, 4):  # First 3 pages
            try:
                data = MovieService.get_trending_movies(time_window, page, use_cache=False)
                if data:
                    print(f"✓ Cached trending {time_window} movies page {page}")
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"✗ Failed to cache trending {time_window} page {page}: {e}")

def warmup_popular_movies():
    """Warmup popular movies cache"""
    print("Warming up popular movies cache...")
    for page in range(1, 4):  # First 3 pages
        try:
            data = MovieService.get_popular_movies(page, use_cache=False)
            if data:
                print(f"✓ Cached popular movies page {page}")
            time.sleep(0.5)
        except Exception as e:
            print(f"✗ Failed to cache popular movies page {page}: {e}")

def warmup_user_recommendations():
    """Warmup personalized recommendations for active users"""
    print("Warming up user recommendations...")
    active_users = User.objects.filter(
        models.Q(favorite_movies__isnull=False) | 
        models.Q(movie_ratings__isnull=False)
    ).distinct()[:50]  # Top 50 active users
    
    for user in active_users:
        try:
            recommendations = MovieService.get_personalized_recommendations(user, 20)
            if recommendations:
                print(f"✓ Generated recommendations for user {user.id}")
            time.sleep(0.1)
        except Exception as e:
            print(f"✗ Failed to generate recommendations for user {user.id}: {e}")

if __name__ == '__main__':
    print("Starting cache warmup...")
    start_time = time.time()
    
    warmup_trending_movies()
    warmup_popular_movies()
    warmup_user_recommendations()
    
    duration = time.time() - start_time
    print(f"Cache warmup completed in {duration:.2f} seconds!")
