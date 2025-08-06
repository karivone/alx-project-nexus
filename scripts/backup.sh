#!/bin/bash

# Database backup script
set -e

BACKUP_DIR="/backup"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="movie_recommendation_db"

echo "📋 Starting database backup..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
echo "🗄️ Backing up PostgreSQL database..."
docker-compose exec -T db pg_dump -U postgres $DB_NAME > "$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Redis backup
echo "💾 Backing up Redis data..."
docker-compose exec -T redis redis-cli BGSAVE
docker cp $(docker-compose ps -q redis):/data/dump.rdb "$BACKUP_DIR/redis_backup_$TIMESTAMP.rdb"

# Compress backups
echo "🗜️ Compressing backups..."
tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" -C $BACKUP_DIR db_backup_$TIMESTAMP.sql redis_backup_$TIMESTAMP.rdb

# Clean up individual files
rm "$BACKUP_DIR/db_backup_$TIMESTAMP.sql" "$BACKUP_DIR/redis_backup_$TIMESTAMP.rdb"

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed: backup_$TIMESTAMP.tar.gz"
