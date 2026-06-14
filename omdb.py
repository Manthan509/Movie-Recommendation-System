import requests
import re

API_KEY = "7a10124c43a357ddce834f70877e3804"

def fetch_movie(movie_name):

    clean_name = re.sub(r"\(\d{4}\)", "", movie_name).strip()

    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={API_KEY}&query={clean_name}"
    )

    response = requests.get(url)

    data = response.json()

    if len(data["results"]) == 0:
        return None

    movie = data["results"][0]

    poster = (
        "https://image.tmdb.org/t/p/w500"
        + movie["poster_path"]
        if movie["poster_path"]
        else None
    )

    return {
        "title": movie["title"],
        "rating": movie["vote_average"],
        "overview": movie["overview"],
        "poster": poster,
        "release_date": movie["release_date"]
    }