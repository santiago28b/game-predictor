import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import plotly.express as px
from wc_sim import calculate_weighted_rating, simulate_match_n

st.set_page_config(page_title="World Cup Simulator", page_icon="⚽", layout="centered")
st.title("⚽ World Cup Head-to-Head Simulator")
st.caption("Ratings combine current FIFA points with historical World Cup titles.")


@st.cache_data
def load_data():
    ranks = pd.read_csv("data/rankings.csv")
    titles = pd.read_csv("data/titles.csv")
    return calculate_weighted_rating(ranks, titles)


df_weighted = load_data()
teams = df_weighted["name"].tolist()

st.subheader("Pick two teams")
col1, col2 = st.columns(2)
with col1:
    team_a = st.selectbox("Team A", teams, index=teams.index("Brazil"))
with col2:
    team_b = st.selectbox("Team B", teams, index=teams.index("Argentina"))

n_sims = st.slider("Number of simulations", min_value=100, max_value=10_000, value=1_000, step=100)

if st.button("Run Simulation"):
    if team_a == team_b:
        st.error("Please select two different teams.")
    else:
        results = simulate_match_n(team_a, team_b, df_weighted, n=n_sims)

        st.subheader("Results")
        col1, col2 = st.columns(2)
        row_a = results[results["team"] == team_a].iloc[0]
        row_b = results[results["team"] == team_b].iloc[0]
        col1.metric(team_a, f"{row_a['win_pct']}%", f"{row_a['wins']} wins")
        col2.metric(team_b, f"{row_b['win_pct']}%", f"{row_b['wins']} wins")

        fig = px.bar(
            results,
            x="team",
            y="win_pct",
            text="win_pct",
            labels={"win_pct": "Win %", "team": ""},
            color="team",
            color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(showlegend=False, yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Weighted Ratings")
        st.dataframe(
            df_weighted[df_weighted["name"].isin([team_a, team_b])][
                ["rank", "name", "points", "wc_titles", "weighted_rating"]
            ].reset_index(drop=True),
            use_container_width=True,
        )
