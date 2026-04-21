# game-predictor
Predict international soccer match outcomes using FIFA rankings and historical World Cup data.

## Resources

- [Documentation](https://santiago28b.github.io/game-predictor/wc_sim.html)
- [Tutorial (Getting Started)](#getting-started)
- [Technical Report](#technical-report)
- [Streamlit App](https://game-predictor-g66jsocnan5fdee67p8ben.streamlit.app/)

---

## Getting Started

### Installation

Clone the repository and install the package using `uv`:

```bash
git clone https://github.com/santiago28b/game-predictor.git
cd game-predictor
uv pip install -e .
```

### Requirements

- Python 3.13+
- Dependencies are managed via `uv` and listed in `pyproject.toml`

### Basic Usage

**1. Build the weighted ratings dataset**

```python
import pandas as pd
from wc_sim import calculate_weighted_rating

ranks  = pd.read_csv("data/rankings.csv")
titles = pd.read_csv("data/titles.csv")

df_weighted = calculate_weighted_rating(ranks, titles, weight=50)
print(df_weighted.head())
```

**2. Simulate a head-to-head match**

```python
from wc_sim import simulate_match

winner = simulate_match("Brazil", "Argentina", df_weighted)
print(winner)
```

**3. Run N simulations and get win percentages**

```python
from wc_sim import simulate_match_n

results = simulate_match_n("Brazil", "Argentina", df_weighted, n=1000)
print(results)
```

**4. Validate the weighted rating against historical data**

```python
from wc_sim import validate_weighted_rating

# results_df is the Kaggle international football results dataset
summary = validate_weighted_rating(results_df, df_weighted)
print(summary)
```

### Running the Streamlit App

```bash
uv run streamlit run app.py
```

---

## Technical Report

### Motivating Question

> **Can we build a more accurate World Cup match simulator by combining a team's current FIFA ranking with its historical World Cup success?**

Standard FIFA/Elo ratings capture current form but ignore tournament pedigree. A team like Brazil may be ranked 6th today, yet historically outperforms that rank on the biggest stage. This project investigates whether adding a "prestige bonus" for past World Cup titles produces a more predictive rating.

### Methodology

**Data Sources**

- **FIFA Rankings** (Zyla Labs API) — current points and rank for 211 national teams.
- **World Cup Titles** — a curated table of the 8 nations that have won the World Cup and their title counts.
- **Historical Match Results** (Kaggle: `martj42/international-football-results-from-1872-to-2017`) — over 40,000 international matches used for validation.

**Weighted Rating Formula**

A custom metric was engineered by merging the two ranking sources:

$$\text{weighted\_rating} = \text{FIFA points} + (\text{WC titles} \times 50)$$

The weight of 50 was chosen so that historical titles influence but do not override current form — no team shifts more than a few positions in the rankings due to heritage alone.

**Validation**

The weighted rating was tested against historical match outcomes. For each match where both teams appeared in the current rankings, we checked whether the higher-rated team won. Raw FIFA points predicted the correct winner in **59.84%** of matches; the weighted rating improved this to **60.85%**, confirming that the transformation adds predictive value.

**Simulation**

Win probability for a head-to-head match is computed as:

$$P(A \text{ wins}) = \frac{\text{rating}_A}{\text{rating}_A + \text{rating}_B}$$

A single match outcome is drawn from this probability. Running the simulation 1,000+ times yields stable win percentage estimates.

### Key Takeaways

- Brazil's 5 World Cup titles add 250 points to its rating, pushing it above several teams with a higher current FIFA rank — consistent with its historically strong tournament performances.
- The weighted rating outperforms raw FIFA points as a match predictor, validating the methodology.
- The simulation is fully reproducible: given the same input CSVs, every user gets the same probability estimates (though individual match outcomes vary by design due to randomness).

### Reproducibility

All data wrangling, validation, and simulation logic lives in the `src/wc_sim/` package. The notebook `scraper.ipynb` documents the data collection steps. Running `app.py` requires only the two CSVs in `data/` and the installed package — no API key is needed after the initial data pull.
