import json
import pandas as pd
import os
from glob import glob

# Hitta senaste raw-filen
files = sorted(glob('data/raw_fantasy_*.json'))
latest = files[-1]
print(f"Processar: {latest}")

# Ladda data
with open(latest) as f:
    raw = json.load(f)

df = pd.DataFrame(raw['results'])

# Genre mapping
genre_map = {
    28: 'Action', 12: 'Äventyr', 14: 'Fantasy',
    878: 'Sci-Fi', 16: 'Animerat', 35: 'Komedi',
    18: 'Drama', 27: 'Skräck', 10751: 'Familj'
}

# Transformera
df['genres'] = df['genre_ids'].apply(lambda x: ', '.join([genre_map.get(i, str(i)) for i in x]))
df['release_year'] = pd.to_datetime(df['release_date']).dt.year
df['release_month'] = pd.to_datetime(df['release_date']).dt.month

# Välj relevanta kolumner
df_clean = df[[
    'id', 'title', 'release_date', 'release_year',
    'release_month', 'popularity', 'vote_average',
    'vote_count', 'genres', 'original_language', 'overview'
]]

# Spara
os.makedirs('data/processed', exist_ok=True)
df_clean.to_csv('data/processed/movies.csv', index=False)
print(f"Sparade {len(df_clean)} filmer till data/processed/movies.csv")