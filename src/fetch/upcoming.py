import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

from src.config import RAW_DIR

load_dotenv()


def fetch_upcoming_fantasy(pages=5):
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise ValueError("Ingen API-nyckel i .env")

    all_movies = []
    today = datetime.now().strftime("%Y-%m-%d")

    for page in range(1, pages + 1):
        print(f"Hämtar sida {page}/{pages}...")

        url = (
            "https://api.themoviedb.org/3/discover/movie"
            f"?api_key={api_key}"
            "&with_genres=14"
            f"&primary_release_date.gte={today}"
            "&sort_by=primary_release_date.asc"
            f"&page={page}"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if "results" in data:
                all_movies.extend(data["results"])

        except requests.RequestException as e:
            print(f"Fel sida {page}: {e}")

    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = Path(RAW_DIR) / f"upcoming_fantasy_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

    print(f"Sparade {len(all_movies)} kommande filmer → {filename}")