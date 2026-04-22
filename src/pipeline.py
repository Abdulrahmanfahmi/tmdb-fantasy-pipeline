from src.fetch.fantasy import save_fantasy_movies
from src.fetch.upcoming import fetch_upcoming_fantasy
from src.fetch.details import fetch_movie_details

from src.utils.movie_ids import load_movie_ids

from src.process.fantasy import process_fantasy
from src.process.upcoming import process_upcoming
from src.process.details import process_movie_details

from src.db.database import load_csv_to_db


def run_pipeline():
    print("Startar pipeline...\n")

    
    print("Steg 1 – Fetch fantasy")
    save_fantasy_movies()

    print("\nSteg 2 – Fetch upcoming")
    fetch_upcoming_fantasy()

    print("\nSteg 3 – Process fantasy")
    process_fantasy()

    print("\nSteg 4 – Process upcoming")
    process_upcoming()

    
    print("\nSteg 5 – Fetch movie details")

    try:
        ids = load_movie_ids() or []

        if len(ids) == 0:
            print("Inga movie IDs hittades")
        else:
            fetch_movie_details(ids[:100])

    except Exception as e:
        print(f"Details fetch failade: {e}")

    print("\nSteg 6 – Process movie details")

    try:
        process_movie_details()
    except Exception as e:
        print(f"Details processing failade: {e}")

    
    print("\nSteg 7 – Load to DuckDB")

    try:
        load_csv_to_db()
    except Exception as e:
        print(f"DB load failade: {e}")

    print("\nPipeline klar!")


if __name__ == "__main__":
    run_pipeline()