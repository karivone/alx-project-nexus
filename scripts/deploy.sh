#!/bin/bash

# Production deployment script
set -e

echo "🚀 Starting deployment..."

# Environment variables
export DJANGO_SETTINGS_MODULE=movie_backend.settings
export DJANGO_ENV=production

# Update code
echo "📦 Pulling latest code..."
git pull origin main

# Build and start containers
echo "🐳 Building Docker containers..."
docker-compose -f docker-compose.prod.yml build

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose.prod.yml run --rm web python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput

# Sync movies data
echo "🎬 Syncing movie data..."
docker-compose -f docker-compose.prod.yml run --rm web python manage.py sync_popular_movies --pages 5

# Warm up cache
echo "🔥 Warming up cache..."
docker-compose -f docker-compose.prod.yml run --rm web python scripts/cache_warmup.py

# Start services
echo "▶️ Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Health check
echo "🏥 Running health checks..."
sleep 30
curl -f http://localhost/health/ || exit 1

echo "✅ Deployment completed successfully!"
echo "🌐 Application is running at: http://localhost"
echo "📚 API documentation: http://localhost/api/docs/"
