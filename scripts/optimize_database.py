#!/usr/bin/env python
"""Database optimization script"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_backend.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def create_indexes():
    """Create additional database indexes for performance"""
    with connection.cursor() as cursor:
        indexes = [
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_popularity_desc ON movies_movie (popularity DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_vote_average_desc ON movies_movie (vote_average DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_release_date_desc ON movies_movie (release_date DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_favorites_created_at ON movies_user_favorite (created_at DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_ratings_rating ON movies_user_rating (rating);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_ratings_updated_at ON movies_user_rating (updated_at DESC);",
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
                print(f"✓ Created index: {index_sql}")
            except Exception as e:
                print(f"✗ Failed to create index: {e}")

def analyze_tables():
    """Analyze tables for query optimization"""
    with connection.cursor() as cursor:
        tables = [
            'movies_movie',
            'movies_user_favorite',
            'movies_user_rating',
            'movies_user_watchlist',
            'auth_user'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"ANALYZE {table};")
                print(f"✓ Analyzed table: {table}")
            except Exception as e:
                print(f"✗ Failed to analyze table {table}: {e}")

if __name__ == '__main__':
    print("Starting database optimization...")
    create_indexes()
    analyze_tables()
    print("Database optimization completed!")
