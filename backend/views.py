import os
import requests
from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Movie Recommendation API!")

def movies(request):
    TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'dabc96b5a972e54425d4efd3010e893d')
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    movies = response.json().get('results', [])
    return render(request, 'movies.html', {'movies': movies})