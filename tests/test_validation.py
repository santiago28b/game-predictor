import pandas as pd
import pytest
from wc_sim import validate_weighted_rating


@pytest.fixture
def sample_data():
    results = pd.DataFrame({
        "home_team": ["Brazil", "Canada"],
        "away_team": ["Canada", "Brazil"],
        "home_score": [2.0, 1.0],
        "away_score": [0.0, 0.0],
    })
    df_weighted = pd.DataFrame({
        "rank": [1, 2],
        "name": ["Brazil", "Canada"],
        "points": [2000.0, 1000.0],
        "wc_titles": [5, 0],
        "weighted_rating": [2250.0, 1000.0],
    })
    return results, df_weighted


def test_output_has_required_columns(sample_data):
    results, df_weighted = sample_data
    summary = validate_weighted_rating(results, df_weighted)
    for col in ["metric", "correct_predictions", "total_matches", "accuracy_pct"]:
        assert col in summary.columns


def test_both_metrics_present(sample_data):
    results, df_weighted = sample_data
    summary = validate_weighted_rating(results, df_weighted)
    assert set(summary["metric"]) == {"points", "weighted_rating"}


def test_accuracy_between_0_and_100(sample_data):
    results, df_weighted = sample_data
    summary = validate_weighted_rating(results, df_weighted)
    assert (summary["accuracy_pct"] >= 0).all()
    assert (summary["accuracy_pct"] <= 100).all()


def test_draws_are_excluded(sample_data):
    results, df_weighted = sample_data
    draw = pd.DataFrame({
        "home_team": ["Brazil"], "away_team": ["Canada"],
        "home_score": [1.0], "away_score": [1.0],
    })
    results_with_draw = pd.concat([results, draw], ignore_index=True)
    summary = validate_weighted_rating(results_with_draw, df_weighted)
    assert summary["total_matches"].values[0] == 2
