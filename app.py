from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'dabc96b5a972e54425d4efd3010e893d')

@app.route('/')
def home():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    movies = response.json().get('results', [])
    return render_template_string('''
        <html>
        <head>
            <title>Popular Movies</title>
            <style>
                body { font-family: Arial, sans-serif; background: #181818; color: #fff; margin: 0; }
                h1 { text-align: center; margin-top: 30px; }
                .grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 24px;
                    padding: 40px;
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .movie-card {
                    background: #222;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                    text-align: center;
                    transition: transform 0.2s;
                }
                .movie-card:hover {
                    transform: scale(1.03);
                }
                .movie-poster {
                    width: 100%;
                    height: 300px;
                    object-fit: cover;
                    background: #333;
                }
                .movie-title {
                    font-size: 1.1em;
                    margin: 16px 0 8px 0;
                    color: #fff;
                }
                .movie-date {
                    color: #bbb;
                    font-size: 0.95em;
                    margin-bottom: 16px;
                }
            </style>
        </head>
        <body>
            <h1>Popular Movies</h1>
            <div class="grid">
            {% for movie in movies %}
                <div class="movie-card">
                    {% if movie['poster_path'] %}
                        <img class="movie-poster" src="https://image.tmdb.org/t/p/w500{{ movie['poster_path'] }}" alt="{{ movie['title'] }}">
                    {% else %}
                        <div class="movie-poster"></div>
                    {% endif %}
                    <div class="movie-title">{{ movie['title'] }}</div>
                    <div class="movie-date">{{ movie['release_date'] }}</div>
                </div>
            {% endfor %}
            </div>
        </body>
        </html>
    ''', movies=movies)

if __name__ == '__main__':
    app.run(port=5000)