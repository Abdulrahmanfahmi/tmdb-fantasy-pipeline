import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

from src.config import RAW_DIR

load_dotenv()


def save_fantasy_movies(pages=50):
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise ValueError("Missing TMDB_API_KEY")

    all_movies = []

    for page in range(1, pages + 1):
        print(f"Hämtar sida {page}/{pages}...")

        url = (
            "https://api.themoviedb.org/3/discover/movie"
            f"?api_key={api_key}"
            "&with_genres=14"
            "&sort_by=popularity.desc"
            f"&page={page}"
        )

        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            all_movies.extend(data.get("results", []))

        except Exception as e:
            print(f"Fel sida {page}: {e}")

    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = Path(RAW_DIR) / f"raw_fantasy_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

    print(f"Sparade {len(all_movies)} filmer → {filename}")