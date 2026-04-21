import pandas as pd


def validate_weighted_rating(results_df: pd.DataFrame, df_weighted: pd.DataFrame) -> pd.DataFrame:
    """
    Validates whether weighted_rating predicts match outcomes better than raw points.

    Merges historical results with current ratings, then computes how often
    the higher-rated team (by each metric) won.

    Args:
        results_df: Kaggle match history with columns
                    ['home_team', 'away_team', 'home_score', 'away_score'].
        df_weighted: Output of calculate_weighted_rating(), must have
                     ['name', 'points', 'weighted_rating'].

    Returns:
        DataFrame with columns ['metric', 'correct_predictions', 'total_matches', 'accuracy_pct'].
    """
    ratings = df_weighted.set_index("name")[["points", "weighted_rating"]]

    df = results_df[["home_team", "away_team", "home_score", "away_score"]].copy()

    # keep only matches where both teams are in our ratings
    known = ratings.index
    df = df[df["home_team"].isin(known) & df["away_team"].isin(known)]

    # drop draws
    df = df[df["home_score"] != df["away_score"]].copy()

    df["winner"] = df.apply(
        lambda r: r["home_team"] if r["home_score"] > r["away_score"] else r["away_team"],
        axis=1,
    )

    for metric in ["points", "weighted_rating"]:
        df[f"{metric}_home"] = df["home_team"].map(ratings[metric])
        df[f"{metric}_away"] = df["away_team"].map(ratings[metric])
        df[f"{metric}_predicted"] = df.apply(
            lambda r, m=metric: r["home_team"] if r[f"{m}_home"] > r[f"{m}_away"] else r["away_team"],
            axis=1,
        )
        df[f"{metric}_correct"] = df["winner"] == df[f"{metric}_predicted"]

    total = len(df)
    rows = []
    for metric in ["points", "weighted_rating"]:
        correct = df[f"{metric}_correct"].sum()
        rows.append({
            "metric": metric,
            "correct_predictions": int(correct),
            "total_matches": total,
            "accuracy_pct": round(correct / total * 100, 2),
        })

    return pd.DataFrame(rows)
