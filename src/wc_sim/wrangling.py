import pandas as pd


def _check_required_columns(df: pd.DataFrame, required: list[str], df_name: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{df_name} is missing required columns: {missing}")


def calculate_weighted_rating(
    rank_df: pd.DataFrame,
    titles_df: pd.DataFrame,
    weight: int = 50
) -> pd.DataFrame:
    """
    Combines current FIFA points with historical World Cup titles into a weighted rating.

    Args:
        rank_df:
            DataFrame with columns ['rank', 'name', 'points'].
        titles_df:
            DataFrame with columns ['team', 'wc_titles'].
        weight:
            Points added per World Cup title. Default is 50.

    Returns:
        A DataFrame with:
        ['fifa_rank', 'name', 'points', 'wc_titles', 'weighted_rating', 'weighted_rank']
    """
    _check_required_columns(rank_df, ["rank", "name", "points"], "rank_df")
    _check_required_columns(titles_df, ["team", "wc_titles"], "titles_df")

    if weight < 0:
        raise ValueError("weight must be non-negative")

    combined = rank_df.copy()

    combined = combined.rename(columns={"rank": "fifa_rank"})

    combined = pd.merge(
        combined,
        titles_df,
        left_on="name",
        right_on="team",
        how="left",
    ).drop(columns="team")

    combined["wc_titles"] = combined["wc_titles"].fillna(0).astype(int)
    combined["weighted_rating"] = combined["points"] + (combined["wc_titles"] * weight)

    combined = combined.sort_values(
        by="weighted_rating",
        ascending=False
    ).reset_index(drop=True)

    combined["weighted_rank"] = combined.index + 1

    return combined[["fifa_rank", "name", "points", "wc_titles", "weighted_rating", "weighted_rank"]]


def compare_rank_changes(df_weighted: pd.DataFrame) -> pd.DataFrame:
    """
    Compares original FIFA rank with weighted rank.

    Args:
        df_weighted:
            Output of calculate_weighted_rating().

    Returns:
        DataFrame sorted by biggest rank change, with:
        ['name', 'fifa_rank', 'weighted_rank', 'rank_change']
    """
    _check_required_columns(
        df_weighted,
        ["name", "fifa_rank", "weighted_rank"],
        "df_weighted"
    )

    out = df_weighted[["name", "fifa_rank", "weighted_rank"]].copy()
    out["rank_change"] = out["fifa_rank"] - out["weighted_rank"]
    out = out.sort_values(by="rank_change", ascending=False).reset_index(drop=True)
    return out
