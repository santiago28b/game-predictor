import pandas as pd
import pytest

from wc_sim import validate_weighted_rating, tune_weight


@pytest.fixture
def sample_data():
    results = pd.DataFrame({
        "home_team": ["Brazil", "Canada", "Brazil"],
        "away_team": ["Canada", "Brazil", "Germany"],
        "home_score": [2.0, 1.0, 1.0],
        "away_score": [0.0, 0.0, 2.0],
    })

    df_weighted = pd.DataFrame({
        "fifa_rank": [1, 2, 3],
        "name": ["Brazil", "Canada", "Germany"],
        "points": [2000.0, 1000.0, 1900.0],
        "wc_titles": [5, 0, 4],
        "weighted_rating": [2250.0, 1000.0, 2100.0],
        "weighted_rank": [1, 3, 2],
    })

    ranks = pd.DataFrame({
        "rank": [1, 2, 3],
        "name": ["Brazil", "Germany", "Canada"],
        "points": [2000.0, 1900.0, 1000.0],
    })

    titles = pd.DataFrame({
        "team": ["Brazil", "Germany"],
        "wc_titles": [5, 4],
    })

    return results, df_weighted, ranks, titles


def test_output_has_required_columns(sample_data):
    results, df_weighted, _, _ = sample_data
    summary = validate_weighted_rating(results, df_weighted)

    for col in ["metric", "correct_predictions", "total_matches", "accuracy_pct"]:
        assert col in summary.columns


def test_both_metrics_present(sample_data):
    results, df_weighted, _, _ = sample_data
    summary = validate_weighted_rating(results, df_weighted)

    assert set(summary["metric"]) == {"points", "weighted_rating"}


def test_accuracy_between_0_and_100(sample_data):
    results, df_weighted, _, _ = sample_data
    summary = validate_weighted_rating(results, df_weighted)

    assert (summary["accuracy_pct"] >= 0).all()
    assert (summary["accuracy_pct"] <= 100).all()


def test_draws_are_excluded(sample_data):
    results, df_weighted, _, _ = sample_data

    draw = pd.DataFrame({
        "home_team": ["Brazil"],
        "away_team": ["Canada"],
        "home_score": [1.0],
        "away_score": [1.0],
    })

    results_with_draw = pd.concat([results, draw], ignore_index=True)
    summary = validate_weighted_rating(results_with_draw, df_weighted)

    assert summary["total_matches"].iloc[0] == 3


def test_tune_weight_returns_weight_column(sample_data):
    results, _, ranks, titles = sample_data
    tuned = tune_weight(results, ranks, titles, weights=[0, 25, 50])

    assert "weight" in tuned.columns
    assert len(tuned) == 3


def test_empty_valid_matches_raises():
    results = pd.DataFrame({
        "home_team": ["A"],
        "away_team": ["B"],
        "home_score": [1],
        "away_score": [0],
    })

    df_weighted = pd.DataFrame({
        "name": ["Brazil"],
        "points": [2000],
        "weighted_rating": [2250],
    })

    with pytest.raises(ValueError):
        validate_weighted_rating(results, df_weighted)
