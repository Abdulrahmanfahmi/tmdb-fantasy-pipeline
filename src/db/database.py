import duckdb
import pandas as pd
from pathlib import Path
import json
from glob import glob

PROCESSED_DIR = Path("data/processed")
RAW_DETAILS_DIR = Path("data/raw/details")
DB_PATH = Path("data/fantasy_movies.db")


def get_connection():
    return duckdb.connect(str(DB_PATH))



def safe_csv(conn, table, path, cols):
    path = Path(path)

    conn.execute(f"DROP TABLE IF EXISTS {table}")

    if path.exists() and path.stat().st_size > 0:
        conn.execute(f"""
            CREATE TABLE {table} AS 
            SELECT * FROM read_csv_auto('{path}')
        """)
    else:
        print(f"Missing {path} → creating empty table")

        df = pd.DataFrame(columns=cols)
        conn.register("tmp", df)
        conn.execute(f"CREATE TABLE {table} AS SELECT * FROM tmp")



def load_csv_to_db():
    conn = get_connection()

    conn.execute("PRAGMA enable_progress_bar=false")

    
    safe_csv(conn, "movies", PROCESSED_DIR / "movies.csv",
             ["id", "title"])

    safe_csv(conn, "upcoming_movies", PROCESSED_DIR / "upcoming_movies.csv",
             ["id", "title"])

    
    safe_csv(conn, "movie_genres",
             PROCESSED_DIR / "movie_genres.csv",
             ["movie_id", "genre_id"])

    safe_csv(conn, "upcoming_movie_genres",
             PROCESSED_DIR / "upcoming_movie_genres.csv",
             ["movie_id", "genre_id"])

    
    safe_csv(conn, "movie_countries",
             PROCESSED_DIR / "movie_countries.csv",
             ["movie_id", "country_code"])

    safe_csv(conn, "upcoming_movie_countries",
             PROCESSED_DIR / "upcoming_movie_countries.csv",
             ["movie_id", "country_code"])

    
    conn.execute("DROP TABLE IF EXISTS movie_details")

    details_files = sorted(glob(str(RAW_DETAILS_DIR / "*.json")))

    if details_files:
        with open(details_files[-1], encoding="utf-8") as f:
            df = pd.DataFrame(json.load(f))

        
        if "id" not in df.columns and "movie_id" in df.columns:
            df["id"] = df["movie_id"]

        conn.register("details", df)
        conn.execute("CREATE TABLE movie_details AS SELECT * FROM details")

        print(f"Loaded movie_details from {details_files[-1]}")
    else:
        print("No movie_details found")

    print("DuckDB fully loaded without crashes")
    conn.close()



def query(sql: str):
    conn = get_connection()
    df = conn.execute(sql).df()
    conn.close()
    return df