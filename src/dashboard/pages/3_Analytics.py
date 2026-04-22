import streamlit as st
import plotly.express as px
from src.dashboard.data import load_movies

st.title("Analytics")

movies = load_movies()

st.subheader("Popularitet vs Betyg")

fig = px.scatter(
    movies,
    x="popularity",
    y="vote_average",
    size="vote_count",
    hover_name="title"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Budget vs Revenue")

budget_df = movies[
    (movies["budget"] > 0) &
    (movies["revenue"] > 0)
]

fig2 = px.scatter(
    budget_df,
    x="budget",
    y="revenue",
    color="vote_average"
)

st.plotly_chart(fig2, use_container_width=True)