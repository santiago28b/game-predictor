import numpy as np
import pandas as pd


def simulate_match(team_a: str, team_b: str, df_weighted: pd.DataFrame) -> str:
    """
    Simulates a head-to-head match between two teams.

    Args:
        team_a: Name of the first team.
        team_b: Name of the second team.
        df_weighted: Output of calculate_weighted_rating(), must have 'name' and 'weighted_rating'.

    Returns:
        Name of the winning team.
    """
    ratings = df_weighted.set_index("name")["weighted_rating"]

    if team_a not in ratings.index:
        raise ValueError(f"Team not found: {team_a}")
    if team_b not in ratings.index:
        raise ValueError(f"Team not found: {team_b}")

    r_a = ratings[team_a]
    r_b = ratings[team_b]

    prob_a = r_a / (r_a + r_b)

    return team_a if np.random.random() < prob_a else team_b


def simulate_match_n(team_a: str, team_b: str, df_weighted: pd.DataFrame, n: int = 1000) -> pd.DataFrame:
    """
    Simulates a head-to-head match n times and returns win percentages.

    Args:
        team_a: Name of the first team.
        team_b: Name of the second team.
        df_weighted: Output of calculate_weighted_rating().
        n: Number of simulations (default 1000).

    Returns:
        DataFrame with columns ['team', 'wins', 'win_pct'].
    """
    results = [simulate_match(team_a, team_b, df_weighted) for _ in range(n)]
    wins_a = results.count(team_a)
    wins_b = results.count(team_b)
    return pd.DataFrame({
        "team": [team_a, team_b],
        "wins": [wins_a, wins_b],
        "win_pct": [round(wins_a / n * 100, 1), round(wins_b / n * 100, 1)],
    })
