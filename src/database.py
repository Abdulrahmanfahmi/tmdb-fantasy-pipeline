import sqlite3
import pandas as pd
import os

def create_database():
    os.makedirs('../data', exist_ok=True)
    conn = sqlite3.connect('../data/fantasy_movies.db')
    cursor = conn.cursor()

    # Skapa tabell för populära filmer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            release_date TEXT,
            release_year INTEGER,
            release_month INTEGER,
            popularity REAL,
            vote_average REAL,
            vote_count INTEGER,
            genres TEXT,
            original_language TEXT,
            overview TEXT
        )
    ''')

    # Skapa tabell för kommande filmer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS upcoming_movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            release_date TEXT,
            release_year INTEGER,
            release_month INTEGER,
            days_until_release INTEGER,
            popularity REAL,
            vote_average REAL,
            vote_count INTEGER,
            genres TEXT,
            original_language TEXT,
            overview TEXT
        )
    ''')

    conn.commit()
    print("Databas skapad!")
    return conn

def load_csv_to_db():
    conn = create_database()

    # Ladda movies.csv
    df_movies = pd.read_csv('../data/processed/movies.csv')
    df_movies.to_sql('movies', conn, if_exists='replace', index=False)
    print(f"Laddade {len(df_movies)} filmer till movies-tabellen")

    # Ladda upcoming_movies.csv
    df_upcoming = pd.read_csv('../data/processed/upcoming_movies.csv')
    df_upcoming.to_sql('upcoming_movies', conn, if_exists='replace', index=False)
    print(f"Laddade {len(df_upcoming)} kommande filmer till upcoming_movies-tabellen")

    conn.close()
    print("\nAllt sparat till data/fantasy_movies.db!")

def query_db(sql):
    conn = sqlite3.connect('../data/fantasy_movies.db')
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

if __name__ == "__main__":
    load_csv_to_db()

    # Testa några queries
    print("\n--- Top 5 högst betyg ---")
    print(query_db("SELECT title, vote_average, popularity FROM movies ORDER BY vote_average DESC LIMIT 5"))

    print("\n--- Närmaste kommande filmer ---")
    print(query_db("SELECT title, release_date, days_until_release FROM upcoming_movies ORDER BY days_until_release ASC LIMIT 5"))