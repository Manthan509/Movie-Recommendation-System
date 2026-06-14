\import requests
import re

API_KEY = "7a10124c43a357ddce834f70877e3804"


def fetch_movie(movie_name):

    clean_name = re.sub(r"\(\d{4}\)", "", movie_name).strip()

    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={API_KEY}&query={clean_name}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

    except requests.exceptions.RequestException:

        return {
            "title": movie_name,
            "year": "N/A",
            "rating": "N/A",
            "plot": "Could not fetch details.",
            "poster": "N/A"
        }

    if len(data["results"]) == 0:

        return {
            "title": movie_name,
            "year": "N/A",
            "rating": "N/A",
            "plot": "Movie details not found.",
            "poster": "N/A"
        }

    movie = data["results"][0]

    poster = (
        "https://image.tmdb.org/t/p/w500" + movie["poster_path"]
        if movie["poster_path"]
        else "N/A"
    )

    year = (
        movie["release_date"][:4]
        if movie.get("release_date")
        else "N/A"
    )

    return {
        "title": movie.get("title", movie_name),
        "year": year,
        "rating": movie.get("vote_average", "N/A"),
        "plot": movie.get("overview", "N/A"),
        "poster": poster
    }