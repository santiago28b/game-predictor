import pandas as pd


def calculate_weighted_rating(rank_df: pd.DataFrame, titles_df: pd.DataFrame, weight: int = 50) -> pd.DataFrame:
    """
    Combines current FIFA points with historical World Cup titles into a weighted rating.

    Args:
        rank_df: Columns ['rank', 'name', 'points'] — current FIFA rankings.
        titles_df: Columns ['team', 'wc_titles'] — all-time WC title counts.
        weight: Points added per historical title (default 50).

    Returns:
        DataFrame with original columns plus 'wc_titles' and 'weighted_rating'.
    """
    combined = pd.merge(
        rank_df,
        titles_df,
        left_on="name",
        right_on="team",
        how="left",
    ).drop(columns="team")

    combined["wc_titles"] = combined["wc_titles"].fillna(0).astype(int)
    combined["weighted_rating"] = combined["points"] + (combined["wc_titles"] * weight)

    combined = combined.sort_values("weighted_rating", ascending=False).reset_index(drop=True)
    combined["rank"] = combined.index + 1

    return combined
