import streamlit as st
from src.dashboard.data import load_movies, load_upcoming

st.title("Overview")

movies = load_movies()
upcoming = load_upcoming()

st.metric("Totalt filmer", len(movies))
st.metric("Snittbetyg", round(movies["vote_average"].mean(), 2))
st.metric("Kommande filmer", len(upcoming))

st.divider()

st.subheader("Filmer per år")

movies_per_year = movies.groupby("release_year").size()

st.line_chart(movies_per_year)