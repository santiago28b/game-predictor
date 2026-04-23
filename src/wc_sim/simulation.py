import numpy as np
import pandas as pd


def _check_required_columns(df: pd.DataFrame, required: list[str], df_name: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{df_name} is missing required columns: {missing}")


def simulate_match(
    team_a: str,
    team_b: str,
    df_weighted: pd.DataFrame,
    random_state: int | None = None
) -> str:
    """
    Simulates one head-to-head match between two teams.

    Args:
        team_a:
            Name of the first team.
        team_b:
            Name of the second team.
        df_weighted:
            DataFrame with columns ['name', 'weighted_rating'].
        random_state:
            Optional seed for reproducibility.

    Returns:
        Name of the winning team.
    """
    _check_required_columns(df_weighted, ["name", "weighted_rating"], "df_weighted")

    if team_a == team_b:
        raise ValueError("team_a and team_b must be different teams")

    ratings = df_weighted.set_index("name")["weighted_rating"]

    if team_a not in ratings.index:
        raise ValueError(f"Team not found: {team_a}")
    if team_b not in ratings.index:
        raise ValueError(f"Team not found: {team_b}")

    r_a = ratings[team_a]
    r_b = ratings[team_b]

    if r_a <= 0 or r_b <= 0:
        raise ValueError("weighted ratings must be positive")

    prob_a = r_a / (r_a + r_b)

    rng = np.random.default_rng(random_state)
    return team_a if rng.random() < prob_a else team_b


def simulate_match_n(
    team_a: str,
    team_b: str,
    df_weighted: pd.DataFrame,
    n: int = 1000,
    random_state: int | None = None
) -> pd.DataFrame:
    """
    Simulates a match n times and returns win counts and win percentages.

    Args:
        team_a:
            Name of the first team.
        team_b:
            Name of the second team.
        df_weighted:
            DataFrame with columns ['name', 'weighted_rating'].
        n:
            Number of simulations.
        random_state:
            Optional seed for reproducibility.

    Returns:
        DataFrame with columns ['team', 'wins', 'win_pct'].
    """
    _check_required_columns(df_weighted, ["name", "weighted_rating"], "df_weighted")

    if n <= 0:
        raise ValueError("n must be a positive integer")

    if team_a == team_b:
        raise ValueError("team_a and team_b must be different teams")

    ratings = df_weighted.set_index("name")["weighted_rating"]

    if team_a not in ratings.index:
        raise ValueError(f"Team not found: {team_a}")
    if team_b not in ratings.index:
        raise ValueError(f"Team not found: {team_b}")

    r_a = ratings[team_a]
    r_b = ratings[team_b]

    if r_a <= 0 or r_b <= 0:
        raise ValueError("weighted ratings must be positive")

    prob_a = r_a / (r_a + r_b)

    rng = np.random.default_rng(random_state)
    draws = rng.random(n)
    wins_a = int((draws < prob_a).sum())
    wins_b = n - wins_a

    return pd.DataFrame({
        "team": [team_a, team_b],
        "wins": [wins_a, wins_b],
        "win_pct": [round(wins_a / n * 100, 2), round(wins_b / n * 100, 2)],
    })
