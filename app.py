from flask import Flask, render_template_string
import requests

app = Flask(__name__)

TMDB_API_KEY = 'dabc96b5a972e54425d4efd3010e893d'

@app.route('/')
def home():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    movies = response.json().get('results', [])
    return render_template_string('''
        <h1>Popular Movies</h1>
        <ul>
        {% for movie in movies %}
            <li>
                <strong>{{ movie['title'] }}</strong><br>
                <img src="https://image.tmdb.org/t/p/w200{{ movie['poster_path'] }}" alt="{{ movie['title'] }}">
            </li>
        {% endfor %}
        </ul>
    ''', movies=movies)

if __name__ == '__main__':
    app.run(port=5000)