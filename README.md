
# The 2026 Strait of Hormuz Closure

Crude flows, import composition, and retail pass-through in the United States and China.

## Research Question

How did the 2026 Strait of Hormuz closure change crude oil flows and import composition for the US and China relative to a fixed pre-crisis baseline, and how differently did the shock pass through to retail fuel prices in each country?

## Full Write-Up

**[Oil_Research_summary.pdf](docs/Oil_Research_summary.pdf)** — the complete analysis: design, data and validation, results for each of the four sub-questions, synthesis, caveats, and sources.

## Headline Results

|                          |                                                                                                                                                                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Disruption**     | Tanker calls and cargo volumes fell 10–12× against baseline, robust across three baseline definitions.                                                                                                                       |
| **China flows**    | Crude imports 34% below baseline by May 2026 (seasonally adjusted); March indistinguishable from baseline, consistent with the 3–4 week shipping lag. No inventory buffering — refiners cut runs in step with the shortfall. |
| **US flows**       | Total crude imports show no detectable effect. This is a power limit, not a null: with 430 kb/d of exposure against a 340 kb/d noise floor, even a total loss would register at 1.26σ.                                        |
| **US composition** | Gulf-origin imports fell two thirds (2.3σ). Latin America absorbed all of it (3.2σ); Canada, eight times larger with spare capacity, did not move.                                                                           |
| **US adjustment**  | Ran through exports (+1,411 kb/d, 4.2σ) and the SPR (−1,300 kb/d, >10σ), not through import substitution alone.                                                                                                             |
| **Pass-through**   | US pre-crisis pass-through is statistically indistinguishable from complete. China withheld 1,425 ¥/t of gasoline increase ($24.42/bbl) via two Article 7 interventions, then let the formula run untouched.                  |
| **Net**            | US pump prices rose 54% Feb→May; Beijing gasoline rose 26% — despite China holding ~12× the Hormuz exposure.                                                                                                                |

## Repository Structure

```
oil-research/
├── data/
│   ├── raw/                    
│   │   ├── exchange-rates/       # FRED DEXCHUS
│   │   ├── flow-chokepoints/     # WTO DataLab transits
│   │   ├── prices-crude/         # FRED Brent, WTI
│   │   ├── prices-retail-us/     # EIA weekly gasoline, diesel
│   │   ├── prices-retail-china/
│   │   │   └── ndrc-notices/     # 39 adjustment notices, PDF
│   │   ├── quantities-us/        # EIA weekly petroleum supply
│   │   ├── quantities-china/
│   │   │   ├── jodi_data/
│   │   │   └── gacc_table14/     # 13 monthly files, 3 column layouts
│   │   └── trade-flows/          # EIA imports by origin
│   └── processed/                # one file per frequency, never a master table
│       ├── crude-prices-daily.csv
│       ├── hormuz-transits-daily.csv
│       ├── us-quantities-weekly.csv
│       ├── us-retail-prices-weekly.csv
│       ├── us-crude-imports-by-origin-monthly.csv
│       ├── china-quantities-monthly.csv
│       └── china-retail-prices-events.csv
├── scripts/
│   ├── data_collection.py        # EIA and FRED API pulls
│	├── data_cleaning.ipynb
│   └── data_analysis.ipynb
├── docs/
│   ├── Oil_Research_summary.pdf  # the write-up
│   ├── data_inventory.md         # per-file source URLs and retrieval dates
│   ├── chronology_table.xlsx     # 21 sourced events
│	├── introduction.txt		    
│   └── hormuz-2026-readme.tex
├── figures/
│   ├── hormuz-disruption-overview.png
│   ├── us-quantities-bar.png
│   ├── us-crude-import-composition.png
│   ├── us-quantities-trend.png
│	├── chinese-quantities-trends.png
│   ├── passthrough-comparison.png
│   └── what-we-pay-for-in-a-gallon-of-regular-gasoline-diesel.png
└── references/
	└── cost-of-closing-the-strait-of-hormuz-reference.pdf
```

**Data conventions.** One processed file per observation frequency; monthly series are never broadcast onto daily rows. Joins happen at the point of a specific question so the aggregation choice stays visible. Monthly series are stamped at month start. Date columns are `period` for monthly and `date` for daily and weekly.

## Setup

API keys for EIA and FRED are read from a gitignored `.env`; see `.env.example` for the variable names.

```bash
pip install -r requirements.txt
```

Raw data is fetched by `scripts/data_collection.py` and directly downloaded from the web (refer to introduction.tx for sources to each website used), cleaned in `scripts/data_cleaning.ipynb`, and analysed in `scripts/data_analysis.ipynb`.
