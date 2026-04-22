import json
import pandas as pd
from glob import glob
from pathlib import Path

PROCESSED_DIR = Path("data/processed")


def process_movie_details():
    files = sorted(glob("data/raw/details/movie_details_*.json"))

    if not files:
        print("Inga details-filer hittades")
        return

    latest = files[-1]
    print(f"Processar: {latest}")

    with open(latest, encoding="utf-8") as f:
        movies = json.load(f)

    details_list = []
    cast_list = []
    crew_list = []
    countries_list = []
    companies_list = []
    languages_list = []

    for movie in movies:
        movie_id = movie.get("id")
        if not movie_id:
            continue

        
        details_list.append({
            "id": movie_id,
            "title": movie.get("title"),
            "original_language": movie.get("original_language"),
            "overview": movie.get("overview"),
            "runtime": movie.get("runtime"),
            "budget": movie.get("budget"),
            "revenue": movie.get("revenue"),
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
            "release_date": movie.get("release_date"),
        })

        
        for c in movie.get("credits", {}).get("cast") or []:
            cast_list.append({
                "movie_id": movie_id,
                "actor_id": c.get("id"),
                "actor_name": c.get("name"),
                "character": c.get("character"),
                "cast_order": c.get("order"),
            })

        
        for c in movie.get("credits", {}).get("crew") or []:
            crew_list.append({
                "movie_id": movie_id,
                "person_id": c.get("id"),
                "name": c.get("name"),
                "job": c.get("job"),
                "department": c.get("department"),
            })

        
        for c in movie.get("production_countries") or []:
            countries_list.append({
                "movie_id": movie_id,
                "country_code": c.get("iso_3166_1"),
                "country_name": c.get("name"),
            })

        
        for c in movie.get("production_companies") or []:
            companies_list.append({
                "movie_id": movie_id,
                "company_id": c.get("id"),
                "company_name": c.get("name"),
            })

        
        for l in movie.get("spoken_languages") or []:
            languages_list.append({
                "movie_id": movie_id,
                "language_code": l.get("iso_639_1"),
                "language_name": l.get("name"),
            })

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    
    pd.DataFrame(details_list).to_csv(PROCESSED_DIR / "movie_details.csv", index=False)
    pd.DataFrame(cast_list).to_csv(PROCESSED_DIR / "movie_cast.csv", index=False)
    pd.DataFrame(crew_list).to_csv(PROCESSED_DIR / "movie_crew.csv", index=False)
    pd.DataFrame(countries_list).to_csv(PROCESSED_DIR / "movie_countries.csv", index=False)
    pd.DataFrame(companies_list).to_csv(PROCESSED_DIR / "movie_companies.csv", index=False)
    pd.DataFrame(languages_list).to_csv(PROCESSED_DIR / "movie_languages.csv", index=False)

    print("ALL DETAILS SAVED")