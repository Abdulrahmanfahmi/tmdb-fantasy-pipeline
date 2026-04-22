import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_movie_details(movie_ids: list):
    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        print("Saknar API key")
        return

    os.makedirs("data/raw/details", exist_ok=True)

    all_details = []

    for i, movie_id in enumerate(movie_ids):
        print(f"{i+1}/{len(movie_ids)}")

        try:
            url = (
                f"https://api.themoviedb.org/3/movie/{movie_id}"
                f"?api_key={api_key}&append_to_response=credits"
            )

            r = requests.get(url, timeout=10)
            r.raise_for_status()

            data = r.json()

            if data:
                all_details.append(data)

        except Exception as e:
            print(f"Error {movie_id}: {e}")

    filename = (
        f"data/raw/details/movie_details_"
        f"{datetime.now().strftime('%Y-%m-%d')}.json"
    )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_details, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_details)} details → {filename}")