import sys
import os
sys.path.append(os.path.dirname(__file__))

from fetch_fantasy import save_fantasy_movies
from fetch_upcoming import fetch_upcoming_fantasy
from process_fantasy import process_fantasy
from process_upcoming import process_upcoming
from database import load_csv_to_db

def run_pipeline():
    print(" Startar TMDB Fantasy Pipeline...\n")

    print(" Steg 1/4 – Hämtar populära fantasyfilmer...")
    save_fantasy_movies(pages=50)

    print("\n Steg 2/4 – Hämtar kommande fantasyfilmer...")
    fetch_upcoming_fantasy(pages=5)

    print("\n Steg 3/4 – Processar populära filmer...")
    process_fantasy()

    print("\n Steg 4/4 – Processar kommande filmer...")
    process_upcoming()

    print("\n Steg 5/5 – Sparar till databas...")
    load_csv_to_db()

    print("\nPipeline klar!")
    print("   → data/processed/movies.csv")
    print("   → data/processed/upcoming_movies.csv")
    print("   → data/fantasy_movies.db")

if __name__ == "__main__":
    run_pipeline()