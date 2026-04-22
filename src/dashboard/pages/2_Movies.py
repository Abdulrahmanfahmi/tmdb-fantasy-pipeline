import streamlit as st
from src.dashboard.data import load_movies

st.title("Movies")

movies = load_movies()

# Filters
min_rating = st.slider("Min rating", 0.0, 10.0, 5.0)
min_votes = st.slider("Min votes", 0, 1000, 50)

filtered = movies[
    (movies["vote_average"] >= min_rating) &
    (movies["vote_count"] >= min_votes)
]

st.write(f"Visar {len(filtered)} filmer")

st.dataframe(filtered.sort_values("vote_average", ascending=False))