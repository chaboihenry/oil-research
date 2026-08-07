### Data Inventory

Baseline: **28 Feb 2025 – 27 Feb 2026**, fixed. Series start 2019-01 where available.
Date columns: `period` (monthly, month-start) or `date` (daily/weekly).

---

## Processed — what I analyse from

One file per frequency. I never merge across frequencies into a master table. Monthly data on daily rows would invent observations. I join at the point of a question instead.

| File                                       | Freq           | Coverage                 | Contents                                               |
| ------------------------------------------ | -------------- | ------------------------ | ------------------------------------------------------ |
| `crude-prices-daily.csv`                 | Daily          | 2019-01-02 → 2026-07-27 | Brent, WTI, spread. USD/bbl                            |
| `hormuz-transits-daily.csv`              | Daily          | 2019-01-01 → 2026-07-23 | Calls + volumes by vessel type, tanker volume-per-call |
| `us-quantities-weekly.csv`               | Weekly (Fri)   | 2019-01 → 2026-07-27    | 7 flows (kb/d), 4 stocks (kbbl)                        |
| `us-retail-prices-weekly.csv`            | Weekly (Mon)   | 2019-01 → 2026-07-27    | Regular gasoline, ULSD. USD/gal                        |
| `us-crude-imports-by-origin-monthly.csv` | Monthly        | 2019-01 → 2026-05       | ~48 origins × 89 months. MBBL                         |
| `china-quantities-monthly.csv`           | Monthly        | 2019-01 → 2026-06       | JODI intake + imports, GACC qty/value, unit cost       |
| `china-retail-prices-events.csv`         | Per adjustment | 2026-02-03 → 2026-07-31 | 13 NDRC adjustments. Yuan/tonne, Beijing               |

### Traps in the processed files

| File                           | Trap                                                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------------------- |
| `crude-prices-daily`         | Nulls are single-market holidays. I don't impute — a filled price is a trade that never happened |
| `hormuz-transits-daily`      | Zero-call days give an undefined ratio. Masked, not filled                                        |
| `us-quantities-weekly`       | Crude stocks total = ex-SPR + SPR. Use two of three, never all                                    |
| both weekly files              | Different weekdays. Fri vs Mon. They don't merge on date                                          |
| `us-crude-imports-by-origin` | `is_aggregate` flags NUS-Z00/ME0/MN0/MP0. Summing without excluding triple-counts               |
| `china-quantities-monthly`   | Outer join. 77 JODI-only, 12 both, 1 GACC-only                                                    |

---

## Checks I ran

| Check                                       | Result                                                |
| ------------------------------------------- | ----------------------------------------------------- |
| US country sums vs`NUS-Z00`               | Exact, all 89 months. EIA's origin list is exhaustive |
| GACC × 7.32 ÷ days vs JODI kb/d           | Exact in 10 of 12 overlapping months                  |
| NDRC level differences vs announced changes | 24/24 pass, from 2026-02-24 on                        |

## Discrepancies

| Where                       | Size              | Status                          |
| --------------------------- | ----------------- | ------------------------------- |
| JODI vs GACC, Jan 2026      | −14,464 kbbl     | Offsets February. Unresolved    |
| JODI vs GACC, Feb 2026      | +14,508 kbbl      | Same volume, different month    |
| JODI vs GACC, Sep 2025      | 82 kb/d           | Probably a revision. Not chased |
| JODI vs EIA, China refining | 16.4 vs 14.2 mb/d | Definitional. Unresolved        |

The Jan/Feb pair nets to 0.3%. Same barrels, different month attribution. I tested JODI 2019–2025 for a Lunar New Year pattern and found none — Jan 0.967, Feb 0.999 of annual mean. Only one Jan/Feb pair has both sources, so I can't diagnose it. **I use JODI for volumes.** February is my treatment-onset month, so this matters.

---

## Raw — provenance, never edited

### Chokepoints

| Source                          | Freq   | Coverage                 | Units                   |
| ------------------------------- | ------ | ------------------------ | ----------------------- |
| PortWatch calls (chokepoint6)   | Daily  | 2019-01-01 → 2026-07-23 | Vessel counts           |
| PortWatch volumes (chokepoint6) | Daily  | 2019-01-01 → 2026-07-23 | **Metric tonnes** |
| EIA chokepoints                 | Annual | 2020 → 1H2025           | mb/d. Reference only    |

Tanker calls: 42–45/day in 2019 → 2–3/day by Jul 2026.
I dropped PortWatch's 7-day MAs. Window and centring aren't documented.
EIA's file gives the exposure asymmetry: **China 5.4 mb/d vs US 0.43 mb/d**.

### Crude prices

| Series           | Nulls | Note                      |
| ---------------- | ----- | ------------------------- |
| `DCOILBRENTEU` | 56    | Global seaborne benchmark |
| `DCOILWTICO`   | 83    | US inland (Cushing)       |

All nulls are holidays. Neither benchmark is the disrupted grade — Hormuz crude is medium-sour and prices off Dubai/Oman. These are proxies. I say so in methods.

### US retail

| Workbook | Sheets | I used | Why                                          |
| -------- | ------ | ------ | -------------------------------------------- |
| Gasoline | 12     | Data 3 | Regular, All Formulations, US                |
| Diesel   | 6      | Data 5 | ULSD. Data 1 is legacy No 2, superseded 2006 |

Sheets without "Weekly" in the column name are monthly.

### China retail — NDRC

14 PDFs, 13 dates, 2026-02-03 → 2026-07-31.

| Detail            | Value                                                                  |
| ----------------- | ---------------------------------------------------------------------- |
| Grade             | 89-octane gasoline, 0# diesel                                          |
| US comparison     | **Not** comparable in levels. US regular is 87 AKI ≈ 91–92 RON |
| Tax               | Inclusive                                                              |
| Effective         | 24:00 on adjustment date → merge on`effective_date`                 |
| Provincial spread | Fixed offset. Shanghai = Beijing − 20 gasoline, − 30 diesel          |

| Intervention | Implied | Actual | Absorbed |
| ------------ | ------- | ------ | -------- |
| 23 Mar 2026  | +2,205  | +1,160 | 1,045    |
| 7 Apr 2026   | +800    | +420   | 380      |

Total 1,425 yuan/t of gasoline increase absorbed. Roughly $27/bbl not passed to consumers.
Everything from 21 Apr is pure mechanism.
The intervention indicator is the text pattern, not a second document. 23 Mar has a separate notice; 7 Apr states the wedge inline.
I haven't collected the ~24 baseline notices from Feb 2025 – Jan 2026.

### US quantities — EIA WPSR

| Sheet  | Contents             | Used          |
| ------ | -------------------- | ------------- |
| Data 1 | Stocks               | Yes           |
| Data 2 | Flows                | Yes           |
| Data 3 | 4-week avg of Data 2 | No — derived |

Product supplied is an accounting residual, not measured consumption. No origin split.

### China quantities

**JODI Primary, 2019–2026.** Filter `CRUDEOIL` + `REFINOBS`/`TOTIMPSB`, unit `KBD`.

| Trap                | Detail                                                                |
| ------------------- | --------------------------------------------------------------------- |
| `UNIT_MEASURE`    | Must filter. Five units per observation                               |
| `CONVBBL`         | Conversion factor (7,320 bbl/kt), not a quantity. I lost time to this |
| `OBS_VALUE`       | Object dtype.`"-"` = missing                                        |
| `ASSESSMENT_CODE` | All China rows are 3. Not in the published legend                     |

**GACC Table 14, 13 files, 2025-06 → 2026-06.**

| Trap           | Detail                                                                 |
| -------------- | ---------------------------------------------------------------------- |
| Quantity units | 10,000 tonnes                                                          |
| Value units    | US$1,000                                                               |
| Layouts        | Three variants (7/8/9 cols). I locate the commodity row and drop nulls |
| Coverage       | July 2026 not published yet                                            |

| Month    | Intake kb/d | Imports kb/d | Unit cost $/t |
| -------- | ----------- | ------------ | ------------- |
| Jun 2025 | —          | —           | 485           |
| Jan 2026 | 16,415      | 12,011       | —            |
| Feb 2026 | 16,459      | 12,043       | 462           |
| Mar 2026 | 16,257      | 11,802       | 541           |
| Apr 2026 | 13,694      | 9,387        | 744           |
| May 2026 | 12,107      | 7,811        | 807           |
| Jun 2026 | —          | 7,145        | 766           |

Volume −41% YoY by June. Unit cost +66%.
Refined products fell harder than crude: **−48.6% vs −29.0%**.
Chinese refineries run spring turnarounds Mar–May. I decompose seasonally before attributing declines to Hormuz.

### Trade flows — EIA API

`petroleum/move/impcus`, 4,486 rows. Facets `product=EPC0`, `process=IM0`.

| Trap          | Detail                                     |
| ------------- | ------------------------------------------ |
| Units         | Both MBBL and MBBL/D present. Filter one   |
| `area-name` | `NA` parses as NaN unless read as string |
| Key           | Stripped before saving                     |

---

## Excluded

| What                    | Why                                                 |
| ----------------------- | --------------------------------------------------- |
| China imports by origin | No free English source has crude × origin × month |
| Demand elasticities     | Cut from the question at the start                  |
| China SPR               | Unpublished. I won't estimate it                    |
| War-risk premiums       | No clean series                                     |

On China origins: Comtrade has no China monthly detail. GACC Table 16 is value-only at HS 2-digit — Ch. 27 mixes crude, coal, LNG, products — and omits Iraq, Kuwait, Angola. My design is asymmetric by necessity. I state it as a limitation rather than hide it.

Related: China reports ~zero crude from Iran ($28k, May 2026) while Malaysia shows $1.83bn of Ch. 27. That's the transshipment channel. "Imports from Iran" isn't a usable series.

---

## Conventions

- Retrieval date in every raw filename
- Monthly series stamped at month start
- 7.32 bbl/tonne for China

**Regime switches:** 28 Feb closure · 8 Apr partial reopen · 18–19 Apr re-close · 17–19 Jun reopen (US–Iran MOU) · Jul breakdown

## Still open

JODI `ASSESSMENT_CODE` 3 · JODI vs EIA refining gap · baseline NDRC notices
