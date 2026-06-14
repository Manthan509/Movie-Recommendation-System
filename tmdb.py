import requests
import re

API_KEY = "7a10124c43a357ddce834f70877e3804"


def fetch_movie(movie_name):

    # Remove year like (2012)
    clean_name = re.sub(r"\(\d{4}\)", "", movie_name)

    # Convert "Avengers, The" -> "The Avengers"
    if ", The" in clean_name:
        clean_name = "The " + clean_name.replace(", The", "")

    clean_name = clean_name.strip()

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

    if not data.get("results"):

        return {
            "title": movie_name,
            "year": "N/A",
            "rating": "N/A",
            "plot": "Movie details not found.",
            "poster": "N/A"
        }

    movie = data["results"][0]

    # Poster
    if movie.get("poster_path"):
        poster = (
            "https://image.tmdb.org/t/p/w500"
            + movie["poster_path"]
        )
    else:
        poster = "N/A"

    # Year
    if movie.get("release_date"):
        year = movie["release_date"][:4]
    else:
        year = "N/A"

    return {
        "title": movie.get("title", movie_name),
        "year": year,
        "rating": movie.get("vote_average", "N/A"),
        "plot": movie.get("overview", "N/A"),
        "poster": poster
    }