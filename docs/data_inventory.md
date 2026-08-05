
# Data Inventory

Baseline: 28 Feb 2025 – 27 Feb 2026 (fixed, never rolling). Series start 2019-01 where available.

## Chokepoint flows

| File                                                  | Source                     | Freq   | Coverage                 | Units / notes                                                                  |
| ----------------------------------------------------- | -------------------------- | ------ | ------------------------ | ------------------------------------------------------------------------------ |
| `transit-calls-portwatch.csv`                       | IMF PortWatch, chokepoint6 | Daily  | 2019-01-01 – 2026-07-23 | Vessel counts by type. Tanker 42–45/day (2019) → 2–3/day (Jul 2026)         |
| `transit-trade-volume-portwatch-imf-2026-08-02.csv` | IMF PortWatch, chokepoint6 | Daily  | 2019-01-01 – 2026-07-23 | Model-estimated volume. Diverges from counts — AIS spoofing/dark vessels      |
| `EIA-chokepoints-hormuz-2026-08-02.xlsx`            | EIA                        | Annual | 2020 – 1H2025           | Reference only, pre-crisis. China 5.4 mb/d vs US 0.43 mb/d Hormuz crude (1H25) |

## Prices — crude

| File                                  | Source               | Freq  | Coverage                 | Units / notes                                                 |
| ------------------------------------- | -------------------- | ----- | ------------------------ | ------------------------------------------------------------- |
| `Crude-Oil-Prices-Brent-Europe.csv` | FRED`DCOILBRENTEU` | Daily | 2019-01-02 – 2026-07-27 | USD/bbl. Global seaborne benchmark                            |
| `Crude-Oil-Prices-WTI.csv`          | FRED`DCOILWTICO`   | Daily | 2019-01-02 – 2026-07-27 | USD/bbl. US inland (Cushing). Spread vs Brent: $3.06 → $8.57 |

Neither benchmark is the disrupted grade (Hormuz crude is medium-sour, prices off Dubai/Oman). Proxy, not direct measure.

## Prices — retail US

| File                                    | Source | Freq         | Coverage              | Units / notes                                    |
| --------------------------------------- | ------ | ------------ | --------------------- | ------------------------------------------------ |
| `EIA-gasoline-regular-2026-08-02.xls` | EIA    | Weekly       | 1990-08 – 2026-07-27 | USD/gal. National + PADD regional                |
| `EIA-diesel-onhighway-2026-08-02.xls` | EIA    | Weekly       | 1994-03 – 2026-07-27 | USD/gal                                          |
| `what-we-pay-for-in-a-gallon...png`   | EIA    | Single month | May 2026              | Illustration only. Gasoline $4.48/gal, 52% crude |

## Prices — retail China

| File                                       | Source  | Freq             | Coverage                 | Units / notes                                                  |
| ------------------------------------------ | ------- | ---------------- | ------------------------ | -------------------------------------------------------------- |
| `ndrc-notices/*.pdf` (12 docs, 11 dates) | NDRC    | ~10 working days | 2026-03-09 – 2026-07-31 | Administered. Beijing tracked                                  |
| `ndrc-adjustments.xlsx`                  | derived | Per adjustment   | same                     | yuan/tonne. Levels reconcile exactly against announced changes |

Grade: 89-octane gasoline, 0# diesel — **not** comparable in levels to US 87 AKI. Tax-inclusive. Effective 24:00 on adjustment date, so merge on `effective_date`. Two interventions (23 Mar, 7 Apr) absorbed 1,045 + 380 yuan/t of gasoline increase vs mechanism. All later adjustments pure mechanism. Missing: last pre-crisis notice (late Feb 2026).

## Quantities — US

| File                                     | Source   | Freq   | Coverage           | Units / notes                                                                                                    |
| ---------------------------------------- | -------- | ------ | ------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `EIA-petroleum-balance-2026-08-02.xls` | EIA WPSR | Weekly | 1982 – 2026-07-27 | Crude imports/exports, refinery net input, product supplied (apparent consumption), stocks, SPR. No origin split |

## Quantities — China

| File                                      | Source           | Freq    | Coverage           | Units / notes                                                                                                                                                                                                                                                                              |
| ----------------------------------------- | ---------------- | ------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `jodi-primary-2019.csv` … `2026.csv` | JODI-Oil Primary | Monthly | 2019-01 – 2026-05 | Filter`CRUDEOIL` + `REFINOBS` (throughput) or `TOTIMPSB` (imports). **Must filter `UNIT_MEASURE`** or rows quintuple. `OBS_VALUE` is object dtype, `"-"` = missing. All China rows `ASSESSMENT_CODE` 3 (undefined in legend — check manual). `CONVBBL` = 7.32 bbl/t |
| `gacc-table14/*.xls` (14 files)         | GACC Table 14    | Monthly | 2025-06 – 2026-06 | **Quantity in 10,000 tonnes, value in US$1,000.** 2026-01 has different column layout — read by header, not position. Jul 2026 not yet published                                                                                                                                    |

Validation: GACC May 2026 crude 3,308 (10,000 t) × 7.32 ÷ 31 = 7,811 kb/d = JODI exactly.

Refinery intake (kb/d): Jan 16,415 · Feb 16,459 · Mar 16,257 · Apr 13,694 · May 12,107
Crude imports (kb/d): Jan 12,011 · Feb 12,043 · Mar 11,802 · Apr 9,387 · May 7,811
Implied unit cost ($/t): Feb 462 → Mar 541 → Apr 744 → May 807 → Jun 766

Chinese refineries run spring turnarounds Mar–May — decompose seasonally before attributing declines to Hormuz.

## Trade flows

| File        | Source                           | Freq    | Coverage | Units / notes                         |
| ----------- | -------------------------------- | ------- | -------- | ------------------------------------- |
| *pending* | EIA API`petroleum/move/impcus` | Monthly | —       | US crude imports by country of origin |

**China origin breakdown deliberately excluded.** No free English source provides crude × origin × month: Comtrade has no China monthly detail; GACC Table 16 is value-only, HS-2-digit (Ch. 27 = crude + coal + LNG + products), and omits Iraq, Kuwait, Angola. Design is asymmetric by necessity — state as a limitation.

Note: China reports ~zero crude from Iran ($28k in May 2026) while Malaysia shows $1.83bn Ch. 27 — the documented transshipment channel. "Imports from Iran" is not a usable series.

## Not measurable / excluded

- Demand elasticities — cut from research question
- China SPR — not published, do not estimate
- War-risk premiums — no clean series; hand-collect dated quotes if needed

## Conventions

- Retrieval date in every raw filename; never edit files in `raw/`
- Conversions: 7.32 bbl/tonne (JODI `CONVBBL`, China-specific)
- Regime switches: 28 Feb closure · 8 Apr partial reopen · 18–19 Apr re-close · 17–19 Jun reopen (US–Iran MOU) · Jul breakdown
