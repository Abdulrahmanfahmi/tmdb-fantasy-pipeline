import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.db.database import query

st.set_page_config(
    page_title="Fantasy Movie Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f0f1a;
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    /* Main background */
    .stApp {
        background-color: #13131f;
        color: #e0e0e0;
    }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #a78bfa;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #a78bfa33;
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e1e32 0%, #252540 100%);
        border: 1px solid #a78bfa33;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #a78bfa;
        line-height: 1;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #9090b0;
        margin-top: 6px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #6060a0;
        margin-top: 4px;
    }

    /* Info box */
    .info-box {
        background: #1e1e32;
        border-left: 3px solid #a78bfa;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        color: #b0b0d0;
    }

    /* Chart containers */
    .chart-box {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 1rem;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c0c0e0", size=12),
    xaxis=dict(gridcolor="#2a2a4a", zerolinecolor="#2a2a4a"),
    yaxis=dict(gridcolor="#2a2a4a", zerolinecolor="#2a2a4a"),
    margin=dict(l=10, r=10, t=30, b=10),
)

@st.cache_data
def load_movies():
    try:
        return query("""
            SELECT
                m.id,
                m.title,
                m.popularity,
                m.vote_average,
                m.vote_count,
                m.genres,
                m.release_year,
                m.release_date,
                m.overview,
                d.budget,
                d.revenue,
                d.runtime,
                d.tagline,
                d.status,
                (
                    SELECT elem['name']
                    FROM UNNEST(d.credits.crew) AS t(elem)
                    WHERE elem['job'] = 'Director'
                    LIMIT 1
                ) AS director
            FROM movies m
            LEFT JOIN movie_details d ON m.id = d.id
            WHERE m.vote_average > 0
              AND m.vote_count > 10
        """)
    except Exception as e:
        st.error(f"Kunde inte ladda filmdata: {e}")
        return pd.DataFrame()

@st.cache_data
def load_upcoming():
    try:
        return query("SELECT * FROM upcoming_movies")
    except Exception as e:
        return pd.DataFrame()

movies = load_movies()
upcoming = load_upcoming()

if movies.empty:
    st.error("Ingen data hittades. Kör load_csv_to_db() först.")
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## Filter")
st.sidebar.markdown("---")

st.sidebar.markdown("**Betyg**")
min_rating = st.sidebar.slider("Minsta betyg", 0.0, 10.0, 5.0, 0.1, label_visibility="collapsed")
st.sidebar.caption(f"Visar filmer med betyg ≥ {min_rating}")

st.sidebar.markdown("**Popularitet & röster**")
min_votes = st.sidebar.slider("Minsta röster", 0, 1000, 50, 10, label_visibility="collapsed")
st.sidebar.caption(f"Minst {min_votes} röster krävs")

st.sidebar.markdown("**Utgivningsår**")
year_min = int(movies["release_year"].min())
year_max = int(movies["release_year"].max())
year_range = st.sidebar.slider("År", year_min, year_max, (year_min, year_max), label_visibility="collapsed")

st.sidebar.markdown("**Genre**")
all_genres = sorted([g for g in movies["genres"].dropna().str.split(", ").explode().unique().tolist() if g])
selected_genre = st.sidebar.selectbox("Genre", ["Alla"] + all_genres, label_visibility="collapsed")

st.sidebar.markdown("**Topp N i stapeldiagram**")
top_n = st.sidebar.slider("Topp N", 5, 30, 15, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:0.75rem;color:#6060a0;'>Data från TMDB API</div>", unsafe_allow_html=True)


filtered = movies[
    (movies["vote_average"] >= min_rating) &
    (movies["vote_count"] >= min_votes) &
    (movies["release_year"] >= year_range[0]) &
    (movies["release_year"] <= year_range[1])
]
if selected_genre != "Alla":
    filtered = filtered[filtered["genres"].str.contains(selected_genre, na=False)]

st.markdown("# Fantasy Movie Dashboard")
st.markdown(
    f"<div class='info-box'>Visar <b>{len(filtered)}</b> filmer "
    f"· Genre: <b>{selected_genre}</b> "
    f"· Betyg ≥ <b>{min_rating}</b> "
    f"· År: <b>{year_range[0]}–{year_range[1]}</b></div>",
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)

avg_rating = filtered["vote_average"].mean() if not filtered.empty else 0
avg_pop = filtered["popularity"].mean() if not filtered.empty else 0
budget_known = filtered[(filtered["budget"].notna()) & (filtered["budget"] > 0)]
avg_runtime = filtered[(filtered["runtime"].notna()) & (filtered["runtime"] > 0)]["runtime"].mean()

with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{len(filtered)}</div>
        <div class='kpi-label'>Filmer</div>
        <div class='kpi-sub'>i urval</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{avg_rating:.1f}</div>
        <div class='kpi-label'>Snittbetyg</div>
        <div class='kpi-sub'>av 10</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{avg_pop:.0f}</div>
        <div class='kpi-label'>Snittpopularitet</div>
        <div class='kpi-sub'>TMDB-poäng</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{int(avg_runtime) if pd.notna(avg_runtime) else "–"}</div>
        <div class='kpi-label'>Snittlängd</div>
        <div class='kpi-sub'>minuter</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{len(upcoming) if not upcoming.empty else 0}</div>
        <div class='kpi-label'>Kommande</div>
        <div class='kpi-sub'>filmer</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("<div class='section-header'> Toppbetyg</div>", unsafe_allow_html=True)
    top_movies = filtered.sort_values("vote_average", ascending=False).head(top_n)
    if not top_movies.empty:
        fig = px.bar(
            top_movies,
            x="vote_average",
            y="title",
            orientation="h",
            color="vote_average",
            color_continuous_scale=["#e05252", "#e0c952", "#52e07a"],
            range_color=[5, 10],
            hover_data={"release_year": True, "vote_count": True, "director": True, "vote_average": ":.1f"},
            labels={"vote_average": "Betyg", "title": ""},
            text="vote_average"
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", textfont_color="#c0c0e0")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c0c0e0", size=12),
            xaxis=dict(gridcolor="#2a2a4a", zerolinecolor="#2a2a4a"),
            yaxis=dict(categoryorder="total ascending", gridcolor="#2a2a4a"),
            margin=dict(l=10, r=10, t=30, b=10),
            coloraxis_showscale=False,
            height=max(350, top_n * 28),
        )
        st.plotly_chart(fig, width="stretch")

with col_right:
    st.markdown("<div class='section-header'>Genre-fördelning</div>", unsafe_allow_html=True)
    genre_counts = (
        filtered["genres"].dropna().str.split(", ").explode()
        .value_counts().reset_index()
    )
    genre_counts.columns = ["genre", "count"]
    if not genre_counts.empty:
        fig_pie = px.pie(
            genre_counts.head(8),
            names="genre",
            values="count",
            color_discrete_sequence=["#a78bfa", "#60a5fa", "#34d399", "#f59e0b", "#f472b6", "#fb923c", "#a3e635", "#22d3ee"],
            hole=0.5
        )
        fig_pie.update_traces(
            textposition="outside",
            textinfo="label+percent",
            textfont_color="#c0c0e0",
            pull=[0.05] + [0] * 7
        )
        fig_pie.update_layout(
            **PLOTLY_THEME,
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig_pie, width="stretch")
        st.caption(f"Baserat på {len(filtered)} filmer · Top 8 genrer visas")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("<div class='section-header'>Popularitetstrend per år</div>", unsafe_allow_html=True)
    st.caption("Snittbetyg och popularitet — hur har fantasy-filmer förändrats över tid?")
    pop_by_year = (
        filtered.groupby("release_year")
        .agg(snitt_popularitet=("popularity", "mean"), snitt_betyg=("vote_average", "mean"), antal=("id", "count"))
        .reset_index()
    )
    if not pop_by_year.empty:
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=pop_by_year["release_year"],
            y=pop_by_year["snitt_popularitet"],
            name="Popularitet",
            line=dict(color="#a78bfa", width=2.5),
            marker=dict(size=6),
            mode="lines+markers",
            hovertemplate="<b>%{x}</b><br>Popularitet: %{y:.1f}<extra></extra>"
        ))
        fig_line.add_trace(go.Scatter(
            x=pop_by_year["release_year"],
            y=pop_by_year["snitt_betyg"] * 10,
            name="Betyg ×10",
            line=dict(color="#34d399", width=2, dash="dot"),
            marker=dict(size=5),
            mode="lines+markers",
            hovertemplate="<b>%{x}</b><br>Betyg: %{customdata:.1f}<extra></extra>",
            customdata=pop_by_year["snitt_betyg"]
        ))
        fig_line.update_layout(
            **PLOTLY_THEME,
            height=320,
            legend=dict(orientation="h", y=1.1, x=0, font=dict(color="#c0c0e0")),
            hovermode="x unified"
        )
        st.plotly_chart(fig_line, width="stretch")

with col_b:
    st.markdown("<div class='section-header'>Popularitet vs Betyg</div>", unsafe_allow_html=True)
    st.caption("Punktstorlek = antal röster. Hover för filmdetaljer.")
    if not filtered.empty:
        fig_scatter = px.scatter(
            filtered,
            x="popularity",
            y="vote_average",
            hover_name="title",
            size="vote_count",
            size_max=30,
            color="vote_average",
            color_continuous_scale=["#e05252", "#e0c952", "#52e07a"],
            range_color=[5, 10],
            hover_data={"release_year": True, "director": True, "vote_count": True, "vote_average": ":.1f"},
            labels={"popularity": "Popularitet →", "vote_average": "Betyg →"},
        )
        fig_scatter.update_layout(
            **PLOTLY_THEME,
            height=320,
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_scatter, width="stretch")

budget_df = filtered[
    (filtered["budget"].notna()) & (filtered["budget"] > 0) &
    (filtered["revenue"].notna()) & (filtered["revenue"] > 0)
].copy()

if not budget_df.empty:
    budget_df["roi"] = ((budget_df["revenue"] - budget_df["budget"]) / budget_df["budget"] * 100).round(1)
    budget_df["vinst"] = budget_df["roi"] > 0

    st.markdown("<div class='section-header'>Budget vs Intäkter</div>", unsafe_allow_html=True)
    st.caption(f"Visar {len(budget_df)} filmer med känd budget och intäkt. Streckad linje = break-even.")

    bc1, bc2, bc3 = st.columns(3)
    vinnare = budget_df[budget_df["roi"] > 0]
    bc1.metric("Filmer med vinst", f"{len(vinnare)} / {len(budget_df)}", f"{len(vinnare)/len(budget_df)*100:.0f}%")
    bc2.metric("Bästa ROI", f"{budget_df['roi'].max():.0f}%", budget_df.loc[budget_df['roi'].idxmax(), 'title'])
    bc3.metric("Sämsta ROI", f"{budget_df['roi'].min():.0f}%", budget_df.loc[budget_df['roi'].idxmin(), 'title'])

    fig_budget = px.scatter(
        budget_df,
        x="budget",
        y="revenue",
        hover_name="title",
        color="roi",
        color_continuous_scale=["#e05252", "#e0c952", "#52e07a"],
        size="vote_average",
        size_max=20,
        hover_data={"director": True, "release_year": True, "roi": ":.0f", "budget": ":,.0f", "revenue": ":,.0f"},
        labels={"budget": "Budget (USD)", "revenue": "Intäkter (USD)", "roi": "ROI %"},
        color_continuous_midpoint=0,
    )
    max_val = max(budget_df["budget"].max(), budget_df["revenue"].max())
    fig_budget.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val,
        line=dict(color="#6060a0", dash="dash", width=1.5))
    fig_budget.add_annotation(x=max_val*0.7, y=max_val*0.65, text="Break-even",
        showarrow=False, font=dict(color="#6060a0", size=11))
    fig_budget.update_layout(**PLOTLY_THEME, height=420, coloraxis_colorbar=dict(title="ROI %"))
    st.plotly_chart(fig_budget, width="stretch")


st.markdown("---")
st.markdown("<div class='section-header'> Sök filmdetaljer</div>", unsafe_allow_html=True)

search = st.text_input("", placeholder="Skriv filmtitel, t.ex. 'Lord of the Rings'...", label_visibility="collapsed")
if search:
    results = filtered[filtered["title"].str.contains(search, case=False, na=False)]
    if results.empty:
        st.info(f"Inga filmer hittades för '{search}'.")
    else:
        st.caption(f"{len(results)} träff(ar)")
        for _, row in results.head(5).iterrows():
            year = int(row["release_year"]) if pd.notna(row["release_year"]) else "?"
            with st.expander(f"{row['title']} ({year}) ·  {row['vote_average']:.1f}/10"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Betyg", f"{row['vote_average']:.1f} / 10")
                c2.metric("Röster", f"{int(row['vote_count']):,}")
                c3.metric("Popularitet", f"{row['popularity']:.1f}")
                if pd.notna(row.get("runtime")) and row.get("runtime", 0) > 0:
                    c4.metric("Längd", f"{int(row['runtime'])} min")
                cols = st.columns(2)
                with cols[0]:
                    if pd.notna(row.get("director")):
                        st.markdown(f"**Regissör:** {row['director']}")
                    if pd.notna(row.get("tagline")) and row.get("tagline"):
                        st.markdown(f"*{row['tagline']}*")
                with cols[1]:
                    if pd.notna(row.get("budget")) and row.get("budget", 0) > 0:
                        st.markdown(f"**Budget:** ${int(row['budget']):,}")
                    if pd.notna(row.get("revenue")) and row.get("revenue", 0) > 0:
                        roi = (row["revenue"] - row["budget"]) / row["budget"] * 100 if row.get("budget", 0) > 0 else None
                        roi_str = f" (ROI: {roi:.0f}%)" if roi is not None else ""
                        st.markdown(f"**Intäkter:** ${int(row['revenue']):,}{roi_str}")
                if pd.notna(row.get("overview")):
                    st.markdown(f"**Synopsis:** {row['overview']}")


if not upcoming.empty:
    st.markdown("---")
    st.markdown("<div class='section-header'> Kommande filmer</div>", unsafe_allow_html=True)
    st.caption(f"{len(upcoming)} filmer planeras. Betyg och popularitet är preliminära.")
    cols_to_show = [c for c in ["title", "release_date", "genres", "vote_average", "popularity"] if c in upcoming.columns]
    st.dataframe(
        upcoming.sort_values("release_date")[cols_to_show].head(20),
        width="stretch",
        hide_index=True,
        column_config={
            "title": st.column_config.TextColumn("Film"),
            "release_date": st.column_config.DateColumn("Premiär"),
            "genres": st.column_config.TextColumn("Genrer"),
            "vote_average": st.column_config.NumberColumn("Betyg", format="%.1f "),
            "popularity": st.column_config.NumberColumn("Popularitet", format="%.1f"),
        }
    )