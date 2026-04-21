import pandas as pd
import pytest
from wc_sim import calculate_weighted_rating


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
    assert result.loc[result["name"] == "Brazil", "weighted_rating"].values[0] == 2000 + 5 * 50
    assert result.loc[result["name"] == "Germany", "weighted_rating"].values[0] == 1900 + 4 * 50


def test_team_with_no_titles_gets_zero(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles)
    canada = result.loc[result["name"] == "Canada"]
    assert canada["wc_titles"].values[0] == 0
    assert canada["weighted_rating"].values[0] == 1800.0


def test_sorted_by_weighted_rating(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles)
    assert result["weighted_rating"].is_monotonic_decreasing


def test_rank_resets_after_sort(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles)
    assert list(result["rank"]) == [1, 2, 3]


def test_output_has_required_columns(sample_data):
    ranks, titles = sample_data
    result = calculate_weighted_rating(ranks, titles)
    for col in ["rank", "name", "points", "wc_titles", "weighted_rating"]:
        assert col in result.columns
