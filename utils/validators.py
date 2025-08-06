"""Custom validators for the movie recommendation app"""

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

def validate_movie_rating(value):
    """Validate movie rating is between 1 and 10"""
    if not isinstance(value, (int, float)):
        raise ValidationError('Rating must be a number')
    
    if not 1 <= value <= 10:
        raise ValidationError('Rating must be between 1 and 10')

def validate_tmdb_id(value):
    """Validate TMDb ID is a positive integer"""
    if not isinstance(value, int) or value <= 0:
        raise ValidationError('TMDb ID must be a positive integer')

def validate_genre_ids(value):
    """Validate genre IDs list"""
    if not isinstance(value, list):
        raise ValidationError('Genre IDs must be a list')
    
    for genre_id in value:
        if not isinstance(genre_id, int) or genre_id <= 0:
            raise ValidationError('Each genre ID must be a positive integer')

def validate_release_year(value):
    """Validate release year is reasonable"""
    if not isinstance(value, int):
        raise ValidationError('Release year must be an integer')
    
    if not 1888 <= value <= 2030:  # First movie was made in 1888
        raise ValidationError('Release year must be between 1888 and 2030')

# Regex validators
tmdb_poster_path_validator = RegexValidator(
    regex=r'^/[a-zA-Z0-9]+\.(jpg|jpeg|png)application = get_asgi_application()
