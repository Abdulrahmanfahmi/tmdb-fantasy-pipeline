import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def save_fantasy_movies(pages=5):
    os.makedirs("data/raw", exist_ok=True)
    
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        print("Hittade ingen API-nyckel! Kolla din .env-fil.")
        return

    all_movies = []

    for page in range(1, pages + 1):
        print(f"Hämtar sida {page}/{pages}...")
        
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres=14&sort_by=popularity.desc&page={page}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_movies.extend(data['results'])
            
        except Exception as e:
            print(f"Fel på sida {page}: {e}")
            break

    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/raw/raw_fantasy_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=4)

    print(f"Sparade {len(all_movies)} filmer till {filename}")

if __name__ == "__main__":
    save_fantasy_movies(pages=50)  