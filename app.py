import streamlit as st
import pandas as pd
import plotly.express as px

from wc_sim import (
    calculate_weighted_rating,
    compare_rank_changes,
    simulate_match_n,
)

st.set_page_config(page_title="Game Predictor", page_icon="⚽", layout="centered")

st.title("⚽ Game Predictor")
st.caption("Ratings combine current FIFA points with historical World Cup titles.")

@st.cache_data
def load_data():
    ranks = pd.read_csv("data/rankings.csv")
    titles = pd.read_csv("data/titles.csv")
    return ranks, titles

ranks, titles = load_data()

st.sidebar.header("Model Settings")

weight = st.sidebar.slider(
    "Points added per World Cup title",
    min_value=0,
    max_value=100,
    value=50,
    step=5,
)

seed = st.sidebar.number_input(
    "Random seed",
    min_value=0,
    value=42,
    step=1,
)

df_weighted = calculate_weighted_rating(ranks, titles, weight=weight)
teams = sorted(df_weighted["name"].tolist())

st.subheader("Pick two teams")

col1, col2 = st.columns(2)

default_a = teams.index("Brazil") if "Brazil" in teams else 0
default_b = teams.index("Argentina") if "Argentina" in teams else min(1, len(teams) - 1)

with col1:
    team_a = st.selectbox("Team A", teams, index=default_a)

with col2:
    team_b = st.selectbox("Team B", teams, index=default_b)

n_sims = st.slider(
    "Number of simulations",
    min_value=100,
    max_value=10000,
    value=1000,
    step=100,
)

if st.button("Run Simulation"):
    if team_a == team_b:
        st.error("Please select two different teams.")
    else:
        results = simulate_match_n(
            team_a,
            team_b,
            df_weighted,
            n=n_sims,
            random_state=int(seed),
        )

        st.subheader("Simulation Results")

        row_a = results.loc[results["team"] == team_a].iloc[0]
        row_b = results.loc[results["team"] == team_b].iloc[0]

        col1, col2 = st.columns(2)
        col1.metric(team_a, f"{row_a['win_pct']}%", f"{row_a['wins']} wins")
        col2.metric(team_b, f"{row_b['win_pct']}%", f"{row_b['wins']} wins")

        fig = px.bar(
            results,
            x="team",
            y="win_pct",
            text="win_pct",
            labels={"team": "", "win_pct": "Win %"},
            color="team",
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(showlegend=False, yaxis_range=[0, 100])
        st.plotly_chart(fig, width="stretch")

        st.subheader("Team Ratings")
        st.dataframe(
            df_weighted[df_weighted["name"].isin([team_a, team_b])][
                ["fifa_rank", "name", "points", "wc_titles", "weighted_rating", "weighted_rank"]
            ].reset_index(drop=True),
            width="stretch",
        )

st.subheader("Biggest Rank Changes")

rank_changes = compare_rank_changes(df_weighted).head(10)
st.dataframe(rank_changes, width="stretch")

fig_changes = px.bar(
    rank_changes,
    x="name",
    y="rank_change",
    labels={"name": "", "rank_change": "Improvement in Rank"},
)
st.plotly_chart(fig_changes, width="stretch")