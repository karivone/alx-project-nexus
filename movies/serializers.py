from rest_framework import serializers
from .models import Movie, UserFavoriteMovie, UserMovieRating, UserWatchlist

class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model"""
    poster_url = serializers.SerializerMethodField()
    backdrop_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'overview', 'release_date',
            'poster_path', 'poster_url', 'backdrop_path', 'backdrop_url',
            'vote_average', 'vote_count', 'popularity', 'genre_ids',
            'adult', 'original_language'
        ]
    
    def get_poster_url(self, obj):
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w500{obj.poster_path}"
        return None
    
    def get_backdrop_url(self, obj):
        if obj.backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280{obj.backdrop_path}"
        return None

class TMDbMovieSerializer(serializers.Serializer):
    """Serializer for TMDb API movie data"""
    id = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField(allow_blank=True)
    release_date = serializers.DateField(allow_null=True)
    poster_path = serializers.CharField(allow_blank=True, allow_null=True)
    backdrop_path = serializers.CharField(allow_blank=True, allow_null=True)
    vote_average = serializers.FloatField()
    vote_count = serializers.IntegerField()
    popularity = serializers.FloatField()
    genre_ids = serializers.ListField(child=serializers.IntegerField())
    adult = serializers.BooleanField()
    original_language = serializers.CharField()
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add full image URLs
        if data.get('poster_path'):
            data['poster_url'] = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        if data.get('backdrop_path'):
            data['backdrop_url'] = f"https://image.tmdb.org/t/p/w1280{data['backdrop_path']}"
        return data

class UserFavoriteMovieSerializer(serializers.ModelSerializer):
    """Serializer for user favorite movies"""
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserFavoriteMovie
        fields = ['id', 'movie', 'movie_id', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')
        try:
            movie = Movie.objects.get(tmdb_id=movie_id)
        except Movie.DoesNotExist:
            raise serializers.ValidationError({"movie_id": "Movie not found"})
        
        validated_data['movie'] = movie
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserMovieRatingSerializer(serializers.ModelSerializer):
    """Serializer for user movie ratings"""
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserMovieRating
        fields = ['id', 'movie', 'movie_id', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')
        try:
            movie = Movie.objects.get(tmdb_id=movie_id)
        except Movie.DoesNotExist:
            raise serializers.ValidationError({"movie_id": "Movie not found"})
        
        validated_data['movie'] = movie
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'movie_id' in validated_data:
            validated_data.pop('movie_id')  # Don't allow movie change on update
        return super().update(instance, validated_data)

class UserWatchlistSerializer(serializers.ModelSerializer):
    """Serializer for user watchlist"""
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserWatchlist
        fields = ['id', 'movie', 'movie_id', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')
        try:
            movie = Movie.objects.get(tmdb_id=movie_id)
        except Movie.DoesNotExist:
            raise serializers.ValidationError({"movie_id": "Movie not found"})
        
        validated_data['movie'] = movie
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
