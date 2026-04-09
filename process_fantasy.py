import json
import pandas as pd
import os
from glob import glob


files = sorted(glob('data/raw/raw_fantasy_*.json'))
latest = files[-1]
print(f"Processar: {latest}")


with open(latest) as f:
    movies = json.load(f)

df = pd.DataFrame(movies)


genre_map = {
    28: 'Action', 12: 'Äventyr', 14: 'Fantasy',
    878: 'Sci-Fi', 16: 'Animerat', 35: 'Komedi',
    18: 'Drama', 27: 'Skräck', 10751: 'Familj'
}


df['genres'] = df['genre_ids'].apply(lambda x: ', '.join([genre_map.get(i, str(i)) for i in x]))
df['release_year'] = pd.to_datetime(df['release_date']).dt.year
df['release_month'] = pd.to_datetime(df['release_date']).dt.month


df_clean = df[[
    'id', 'title', 'release_date', 'release_year',
    'release_month', 'popularity', 'vote_average',
    'vote_count', 'genres', 'original_language', 'overview'
]]


os.makedirs('data/processed', exist_ok=True)
df_clean.to_csv('data/processed/movies.csv', index=False)
print(f"Sparade {len(df_clean)} filmer till data/processed/movies.csv")