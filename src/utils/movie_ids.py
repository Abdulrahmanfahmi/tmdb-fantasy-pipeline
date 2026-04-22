import pandas as pd

def load_movie_ids():
    df = pd.read_csv("data/processed/movies.csv")
    df_upcoming = pd.read_csv("data/processed/upcoming_movies.csv")

    ids = set(df["id"].tolist() + df_upcoming["id"].tolist())
    return list(ids)