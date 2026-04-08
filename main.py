import os
import requests
from dotenv import load_dotenv

# Laddar in .env-filen
load_dotenv()

def check_setup():
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("Hittade ingen API-nyckel i .env-filen!")
        return

    # Gör ett testanrop till TMDb för att hämta Fantasy-genrens ID (14)
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=sv-SE"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Succé! Kopplingen till TMDb fungerar.")
            genres = response.json().get('genres', [])
            for g in genres:
                if g['id'] == 14:
                    print(f"Hittade Fantasy! ID: {g['id']}")
        else:
            print(f"Fel vid anrop: {response.status_code}")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

if __name__ == "__main__":
    check_setup()