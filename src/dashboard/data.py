from src.db.database import query
import pandas as pd
import streamlit as st

@st.cache_data
def load_movies():
    return query("""
        SELECT
            m.id,
            m.title,
            m.popularity,
            m.vote_average,
            m.vote_count,
            m.genres,
            m.release_year,
            d.budget,
            d.revenue,
            d.runtime
        FROM movies m
        LEFT JOIN movie_details d ON m.id = d.id
        WHERE m.vote_average > 0
          AND m.vote_count > 10
    """)

@st.cache_data
def load_upcoming():
    return query("SELECT * FROM upcoming_movies")