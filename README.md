---
title: "Game Predictor"
---


A Python package for simulating international soccer match outcomes using FIFA rankings and historical World Cup success.

---

## Project Overview

This project explores whether match prediction can be improved by combining:

- Current FIFA ranking points
- Historical FIFA World Cup titles

The idea is to create a simple weighted rating system, validate it using historical match results, and use it to simulate head-to-head matchups.

The project follows a full data science workflow:

1. Data collection
2. Data cleaning and preparation
3. Analysis and modeling
4. Validation
5. Communication through documentation, tutorial, report, and app

---

## Links

| Resource            | URL                                                                 |
|---------------------|---------------------------------------------------------------------|
| GitHub Pages Website | https://santiago28b.github.io/game-predictor/                     |
| Tutorial            | https://santiago28b.github.io/game-predictor/tutorial.html         |
| Technical Report    | https://santiago28b.github.io/game-predictor/report.html           |
| API Reference       | https://santiago28b.github.io/game-predictor/reference.html        |
| Streamlit App       | https://game-predictor-g66jsocnan5fdee67p8ben.streamlit.app/       |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/santiago28b/game-predictor.git
cd game-predictor
```

Install the package locally:

```bash
pip install -e .
```

Optional (for development tools):

```bash
pip install -e .[dev]
```

---

## Basic Usage

### Load the data

```python
import pandas as pd
from wc_sim import calculate_weighted_rating

ranks = pd.read_csv("data/rankings.csv")
titles = pd.read_csv("data/titles.csv")
```

### Build the weighted rating table

```python
df_weighted = calculate_weighted_rating(ranks, titles, weight=50)
print(df_weighted.head())
```

This creates a dataset that includes:

- Original FIFA rank
- FIFA points
- World Cup titles
- Weighted rating
- Weighted rank

### Compare ranking changes

```python
from wc_sim import compare_rank_changes

changes = compare_rank_changes(df_weighted)
print(changes.head())
```

### Simulate one match

```python
from wc_sim import simulate_match

winner = simulate_match("Brazil", "Argentina", df_weighted, random_state=42)
print(winner)
```

### Simulate many matches

```python
from wc_sim import simulate_match_n

results = simulate_match_n("Brazil", "Argentina", df_weighted, n=1000, random_state=42)
print(results)
```

### Validate the model

```python
from wc_sim import validate_weighted_rating

# Load your historical match results dataset
results_df = pd.read_csv("path_to_your_results_dataset.csv")

summary = validate_weighted_rating(results_df, df_weighted)
print(summary)
```

This compares prediction accuracy between:

- Raw FIFA points
- Weighted rating

### Tune the title weight

```python
from wc_sim import tune_weight

weight_results = tune_weight(
    results_df,
    ranks,
    titles,
    weights=[0, 25, 50, 75, 100]
)

print(weight_results)
```

This step helps determine how much historical success should influence team ratings.

---

## Streamlit App

Run the app locally:

```bash
streamlit run app.py
```

The app allows users to:

- Select two teams
- Choose the title weight
- Run simulations
- View win probabilities
- Compare ratings
- Explore ranking changes

---

## Repository Structure

```
game-predictor/
├── data/
│   ├── rankings.csv
│   └── titles.csv
├── docs/
├── src/
│   └── wc_sim/
│       ├── __init__.py
│       ├── wrangling.py
│       ├── simulation.py
│       └── validation.py
├── tests/
├── app.py
├── main.py
├── scraper.ipynb
├── README.md
├── pyproject.toml
├── _quarto.yml
├── index.qmd
├── tutorial.qmd
├── report.qmd
└── reference.qmd
```

---

## Reproducibility

This project is fully reproducible and includes:

- Data files in the `data` folder
- A Python package with reusable functions
- Test files to verify correctness
- A notebook documenting data collection and preparation
- A Quarto website with documentation, tutorial, and report
- A Streamlit app for interactive exploration

---

## Project Idea

The main goal of this project is to answer the question:

> Can we improve match prediction by including historical World Cup success in addition to current FIFA rankings?

The weighted rating system is simple, interpretable, and easy to extend.

---

## Limitations

This model is intentionally simple and does not include:

- Draw probabilities
- Home-field advantage
- Injuries or roster changes
- Recent form beyond ranking points
- Advanced metrics such as expected goals

Because of this, it should be viewed as a basic analytical tool rather than a full prediction model.

---

## Conclusion

The `wc-sim` package demonstrates a complete data science workflow:

- Assembling a dataset
- Cleaning and merging data
- Building a simple model
- Validating predictions
- Simulating outcomes
- Communicating results through documentation and an app

The project provides a clear and reproducible framework for exploring how historical performance can influence match predictions.