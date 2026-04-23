import pandas as pd
import pytest

from wc_sim import simulate_match, simulate_match_n


@pytest.fixture
def df_weighted():
    return pd.DataFrame({
        "fifa_rank": [1, 2],
        "name": ["Brazil", "Canada"],
        "points": [2000.0, 1000.0],
        "wc_titles": [5, 0],
        "weighted_rating": [2250.0, 1000.0],
        "weighted_rank": [1, 2],
    })


def test_simulate_match_returns_valid_winner(df_weighted):
    winner = simulate_match("Brazil", "Canada", df_weighted, random_state=42)
    assert winner in ["Brazil", "Canada"]


def test_simulate_match_unknown_team_raises(df_weighted):
    with pytest.raises(ValueError):
        simulate_match("Brazil", "Atlantis", df_weighted)


def test_simulate_match_same_team_raises(df_weighted):
    with pytest.raises(ValueError):
        simulate_match("Brazil", "Brazil", df_weighted)


def test_simulate_match_n_output_shape(df_weighted):
    result = simulate_match_n("Brazil", "Canada", df_weighted, n=100, random_state=42)
    assert len(result) == 2
    assert set(result["team"]) == {"Brazil", "Canada"}


def test_simulate_match_n_win_pct_sums_to_100(df_weighted):
    result = simulate_match_n("Brazil", "Canada", df_weighted, n=1000, random_state=42)
    assert abs(result["win_pct"].sum() - 100.0) < 0.01


def test_simulate_match_n_favors_higher_rated(df_weighted):
    result = simulate_match_n("Brazil", "Canada", df_weighted, n=2000, random_state=42)
    brazil_pct = result.loc[result["team"] == "Brazil", "win_pct"].iloc[0]
    assert brazil_pct > 60


def test_simulate_match_n_invalid_n_raises(df_weighted):
    with pytest.raises(ValueError):
        simulate_match_n("Brazil", "Canada", df_weighted, n=0)
