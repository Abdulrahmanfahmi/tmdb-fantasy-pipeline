import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {"api_key": API_KEY}

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
    except:
        return None