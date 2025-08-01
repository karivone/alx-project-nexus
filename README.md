# Movie Recommendation Backend API

A comprehensive Django REST API for movie recommendations with user management, caching, and TMDb integration.

## Features

- **Movie Data**: Integration with TMDb API for trending, popular, and detailed movie information
- **User Authentication**: JWT-based authentication system
- **User Preferences**: Favorites, ratings, and watchlist management
- **Personalized Recommendations**: AI-driven recommendations based on user preferences
- **High Performance**: Redis caching for optimized API response times
- **Comprehensive Documentation**: Swagger/OpenAPI documentation at `/api/docs`

## Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT (Simple JWT)
- **API Documentation**: drf-yasg (Swagger)
- **External API**: The Movie Database (TMDb)

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis
- TMDb API Key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd movie_recommendation_backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment setup**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Run the server**
```bash
python manage.py runserver
```

### Environment Variables

Create a `.env` file with the following variables:

```env
DEBUG=True
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/movie_recommendation_db
REDIS_URL=redis://localhost:6379/0
TMDB_API_KEY=your-tmdb-api-key-here
TMDB_BASE_URL=https://api.themoviedb.org/3
ALLOWED_HOSTS=localhost,127.0.0.1
```

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET/PUT /api/auth/profile/` - User profile management

### Movie Endpoints

- `GET /api/movies/trending/` - Get trending movies
- `GET /api/movies/popular/` - Get popular movies
- `GET /api/movies/search/` - Search movies
- `GET /api/movies/<movie_id>/` - Get movie details
- `GET /api/movies/<movie_id>/recommendations/` - Get movie recommendations
- `GET /api/movies/recommendations/personalized/` - Get personalized recommendations (auth required)

### User Preference Endpoints

- `GET/POST /api/movies/favorites/` - List/add favorite movies
- `DELETE /api/movies/favorites/<movie_id>/` - Remove from favorites
- `GET/POST /api/movies/ratings/` - List/add movie ratings
- `GET/PUT/DELETE /api/movies/ratings/<movie_id>/` - Manage specific rating
- `GET/POST /api/movies/watchlist/` - List/add to watchlist
- `DELETE /api/movies/watchlist/<movie_id>/` - Remove from watchlist

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`

## Caching Strategy

The application uses Redis for caching with the following TTL values:
- **Trending Movies**: 30 minutes
- **Popular Movies**: 30 minutes
- **Movie Details**: 1 hour
- **Movie Recommendations**: 45 minutes
- **Search Results**: 15 minutes

## Database Schema

### Core Models

1. **User** (Extended Django User)
   - Email-based authentication
   - User preferences and profile information

2. **Movie**
   - Cached movie data from TMDb
   - Optimized for quick lookups and recommendations

3. **UserFavoriteMovie**
   - User's favorite movies
   - Many-to-many relationship with unique constraints

4. **UserMovieRating**
   - User ratings (1-10 scale)
   - Used for personalized recommendations

5. **UserWatchlist**
   - Movies user wants to watch
   - Simple bookmark functionality

## Performance Optimizations

1. **Database Indexing**: Strategic indexes on frequently queried fields
2. **Query Optimization**: Select/prefetch related data to minimize queries
3. **Redis Caching**: Multi-level caching for external API calls
4. **Pagination**: Consistent pagination across all list endpoints
5. **Connection Pooling**: Optimized database connections

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **CORS Configuration**: Controlled cross-origin requests
3. **Input Validation**: Comprehensive request validation
4. **Rate Limiting**: Protection against API abuse
5. **Environment Variables**: Secure configuration management

## Testing

Run the test suite:
```bash
python manage.py test
```

For coverage report:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
