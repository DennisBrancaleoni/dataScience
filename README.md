# Formula 1 World Championship — Data Science Analysis

> End-to-end data science project exploring 75 years of Formula 1 racing history (1950–present) through exploratory data analysis, statistical modeling, and interactive visualizations.

---

## Overview

This project applies data science techniques to the complete Formula 1 historical dataset, uncovering patterns across drivers, constructors, circuits, and race strategies. The analysis spans dataset construction, feature engineering, statistical correlation, and dashboard generation — packaged as a reproducible Jupyter notebook with supporting Python scripts.

---

## Key Analyses

| Analysis | Description |
|---|---|
| **Championship by Team** | Constructor dominance across eras |
| **Driver Win Rate** | Normalized win percentage per driver |
| **Fast Lap Evolution** | Lap time progression over decades |
| **Pit Stop Strategy** | Correlation between pit stop count and final race position |
| **Qualifying vs Race Result** | How grid position predicts race outcome |
| **Team Victories by Decade** | Shifting constructor power across F1 history |
| **Fastest Circuits** | Track-level benchmarking by average lap speed |
| **GP Hosting by Nation** | Geographic distribution of Grand Prix events |

---

## Tech Stack

- **Language:** Python 3
- **Analysis & Modeling:** pandas, NumPy, SciPy
- **Visualization:** Matplotlib, Seaborn
- **Notebook:** Jupyter
- **Dashboard:** Custom multi-panel layout via Matplotlib (`generate_dashboard.py`)
- **Dataset:** Ergast F1 API data — 14 normalized CSV sources unified into a single flat dataset

---

## Project Structure

```
.
├── Formula1WorldChampionshipAnalysis.ipynb   # Main analysis notebook
├── mainDataset.csv                           # Unified dataset (built by unify_files.py)
├── data/                                     # Raw CSV sources (circuits, drivers, results, etc.)
└── scripts/
    ├── unify_files.py                        # Merges raw CSVs into mainDataset.csv
    ├── generate_dashboard.py                 # Renders the F1 overview dashboard
    ├── build_presentation.py                 # Exports presentation-ready charts
    └── *.py                                  # Individual analysis scripts
```

---

## Getting Started

**1. Install dependencies**
```bash
conda install pandas numpy matplotlib seaborn
```
or
```bash
pip install -r requirements.txt
```

**2. Build the unified dataset**
```bash
python scripts/unify_files.py
```

**3. Run the analysis**

Open `Formula1WorldChampionshipAnalysis.ipynb` in Jupyter and run all cells.

---

## Dataset

The dataset covers **every Formula 1 race from 1950 to the present**, sourced from the [Ergast Developer API](http://ergast.com/mrd/). It includes:

- Race results, grid positions, lap counts, and finish times
- Qualifying session times (Q1, Q2, Q3)
- Pit stop counts and total pit time per driver per race
- Driver and constructor championship standings
- Circuit metadata (location, altitude, coordinates)
- Sprint race results

All sources are merged into a single denormalized table (`mainDataset.csv`) for efficient analysis.

---

## Sample Outputs

| Visual | Script |
|---|---|
| F1 Dashboard Overview | `generate_dashboard.py` |
| Fast Lap Evolution (line + boxplot) | `FastlapEvolution.py` |
| Pit Stop Correlation Heatmap | `CorrelationPitstopsFinalPosition.py` |
| Constructor Stacked Bar Chart | `ChampionshipByTeam.py` |
| Races per Country Map | `NationWithMoreGP.py` |

---

## Author

**Dennis Brancaleoni** — Data Science, University project (2nd year, 2nd semester)
