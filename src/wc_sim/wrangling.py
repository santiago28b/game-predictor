import pandas as pd
import pytest

from wc_sim import calculate_weighted_rating, compare_rank_changes


@pytest.fixture
def sample_data():
    ranks = pd.DataFrame({
        "rank": [1, 2, 3],
        "name": ["Brazil", "Germany", "Canada"],
        "points": [2000.0, 1900.0, 1800.0],
    })
    titles = pd.DataFrame({
        "team": ["Brazil", "Germany"],
        "wc_titles": [5, 4],
    })
    return ranks, titles


def test_weighted_rating_formula(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles, weight=50)

    assert result.loc[result["name"] == "Brazil", "weighted_rating"].iloc[0] == 2250.0
    assert result.loc[result["name"] == "Germany", "weighted_rating"].iloc[0] == 2100.0


def test_team_with_no_titles_gets_zero(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles)

    canada = result.loc[result["name"] == "Canada"].iloc[0]
    assert canada["wc_titles"] == 0
    assert canada["weighted_rating"] == 1800.0


def test_output_has_required_columns(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles)

    expected = ["fifa_rank", "name", "points", "wc_titles", "weighted_rating", "weighted_rank"]
    for col in expected:
        assert col in result.columns


def test_weighted_rank_is_monotonic(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles)

    assert list(result["weighted_rank"]) == [1, 2, 3]


def test_compare_rank_changes_returns_expected_columns(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles)
    changes = compare_rank_changes(result)

    expected = ["name", "fifa_rank", "weighted_rank", "rank_change"]
    for col in expected:
        assert col in changes.columns


def test_missing_columns_raise_error(sample_data):
    ranks, titles = sample_data
    bad_ranks = ranks.drop(columns=["points"])

    with pytest.raises(ValueError):
        calculate_weighted_rating(bad_ranks, titles)
