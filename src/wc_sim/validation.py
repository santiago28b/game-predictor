import pandas as pd

from .wrangling import calculate_weighted_rating


def _check_required_columns(df: pd.DataFrame, required: list[str], df_name: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{df_name} is missing required columns: {missing}")


def validate_weighted_rating(
    results_df: pd.DataFrame,
    df_weighted: pd.DataFrame
) -> pd.DataFrame:
    """
    Validates whether weighted_rating predicts match outcomes better than raw FIFA points.

    Args:
        results_df:
            DataFrame with columns
            ['home_team', 'away_team', 'home_score', 'away_score'].
        df_weighted:
            DataFrame with columns ['name', 'points', 'weighted_rating'].

    Returns:
        DataFrame with columns
        ['metric', 'correct_predictions', 'total_matches', 'accuracy_pct'].
    """
    _check_required_columns(
        results_df,
        ["home_team", "away_team", "home_score", "away_score"],
        "results_df"
    )
    _check_required_columns(
        df_weighted,
        ["name", "points", "weighted_rating"],
        "df_weighted"
    )

    ratings = df_weighted.set_index("name")[["points", "weighted_rating"]]

    df = results_df[["home_team", "away_team", "home_score", "away_score"]].copy()

    known = ratings.index
    df = df[df["home_team"].isin(known) & df["away_team"].isin(known)]

    # remove draws in actual match results
    df = df[df["home_score"] != df["away_score"]].copy()

    if df.empty:
        raise ValueError("No valid non-draw matches remain after filtering to known teams.")

    df["winner"] = df.apply(
        lambda r: r["home_team"] if r["home_score"] > r["away_score"] else r["away_team"],
        axis=1,
    )

    rows = []

    for metric in ["points", "weighted_rating"]:
        df[f"{metric}_home"] = df["home_team"].map(ratings[metric])
        df[f"{metric}_away"] = df["away_team"].map(ratings[metric])

        # if ratings tie, count as no prediction
        df[f"{metric}_predicted"] = df.apply(
            lambda r, m=metric:
                r["home_team"] if r[f"{m}_home"] > r[f"{m}_away"]
                else (r["away_team"] if r[f"{m}_away"] > r[f"{m}_home"] else None),
            axis=1
        )

        valid_preds = df[f"{metric}_predicted"].notna()
        correct = (df.loc[valid_preds, "winner"] == df.loc[valid_preds, f"{metric}_predicted"]).sum()
        total = int(valid_preds.sum())

        accuracy = round(correct / total * 100, 2) if total > 0 else 0.0

        rows.append({
            "metric": metric,
            "correct_predictions": int(correct),
            "total_matches": total,
            "accuracy_pct": accuracy,
        })

    return pd.DataFrame(rows)


def tune_weight(
    results_df: pd.DataFrame,
    rank_df: pd.DataFrame,
    titles_df: pd.DataFrame,
    weights: list[int]
) -> pd.DataFrame:
    """
    Tests multiple title weights and returns validation accuracy for each one.

    Args:
        results_df:
            Historical results DataFrame.
        rank_df:
            FIFA rankings DataFrame.
        titles_df:
            World Cup titles DataFrame.
        weights:
            List of candidate weights to test.

    Returns:
        DataFrame with validation results for each tested weight.
    """
    if not weights:
        raise ValueError("weights must contain at least one value")

    rows = []

    for weight in weights:
        df_weighted = calculate_weighted_rating(rank_df, titles_df, weight=weight)
        summary = validate_weighted_rating(results_df, df_weighted)
        weighted_row = summary.loc[summary["metric"] == "weighted_rating"].iloc[0]

        rows.append({
            "weight": weight,
            "correct_predictions": int(weighted_row["correct_predictions"]),
            "total_matches": int(weighted_row["total_matches"]),
            "accuracy_pct": float(weighted_row["accuracy_pct"]),
        })

    return pd.DataFrame(rows).sort_values(
        by="accuracy_pct",
        ascending=False
    ).reset_index(drop=True)
