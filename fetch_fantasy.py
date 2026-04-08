import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

def save_fantasy_movies():
    # 2. Skapa mappen 'data' om den inte finns
    os.makedirs("data", exist_ok=True)
    
    
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("Hittade ingen API-nyckel! Kolla din .env-fil.")
        return

    
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres=14&sort_by=popularity.desc"
    
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Kolla om anropet gick bra
        data = response.json()
        
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"data/raw_fantasy_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Succé! Sparade {len(data['results'])} fantasyfilmer till {filename}")
        
    except Exception as e:
        print(f" Något gick fel vid hämtningen: {e}")

if __name__ == "__main__":
    save_fantasy_movies()

