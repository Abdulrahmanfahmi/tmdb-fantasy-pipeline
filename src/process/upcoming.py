import json
import pandas as pd
from glob import glob
from pathlib import Path

PROCESSED_DIR = Path("data/processed")


def process_upcoming():
    files = sorted(glob("data/raw/upcoming_fantasy_*.json"))

    if not files:
        print("Inga upcoming filer hittades")
        return

    latest = files[-1]
    print(f"Processar: {latest}")

    with open(latest, encoding="utf-8") as f:
        movies = json.load(f)

    df = pd.DataFrame(movies)

    
    genre_map = {
        28: 'Action', 12: 'Adventure', 14: 'Fantasy',
        878: 'Sci-Fi', 16: 'Animation', 35: 'Comedy',
        18: 'Drama', 27: 'Horror', 10751: 'Family'
    }

    df["genre_ids"] = df.get("genre_ids", pd.Series([[]] * len(df)))

    df["genres"] = df["genre_ids"].apply(
        lambda x: ", ".join([genre_map.get(i, str(i)) for i in (x or [])])
    )

    df["release_date"] = pd.to_datetime(df.get("release_date"), errors="coerce")

    df["release_year"] = df["release_date"].dt.year
    df["release_month"] = df["release_date"].dt.month
    df["days_until_release"] = (df["release_date"] - pd.Timestamp.today()).dt.days

    
    df_upcoming = df[[
        "id", "title", "release_date", "release_year",
        "release_month", "days_until_release",
        "popularity", "vote_average", "vote_count",
        "genres", "original_language", "overview"
    ]]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df_upcoming.to_csv(PROCESSED_DIR / "upcoming_movies.csv", index=False)

    print(f"Sparade {len(df_upcoming)} upcoming filmer")

    
    country_rows = []

    for movie in movies:
        for c in movie.get("production_countries") or []:
            country_rows.append({
                "movie_id": movie.get("id"),
                "country_code": c.get("iso_3166_1")
            })

    df_countries = pd.DataFrame(country_rows)

    
    df_countries.to_csv(
        PROCESSED_DIR / "upcoming_movie_countries.csv",
        index=False
    )

    print(f"Countries: {len(df_countries)} rows")