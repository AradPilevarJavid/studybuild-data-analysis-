# Insurance Claims & Portfolio Risk Analytics — Python + Tableau

**StudyBuild — Project 01 | Data Analysis & Business Intelligence Track**

A complete descriptive analytics project analysing 678,000+ French motor third-party liability insurance policies. The project performs data preparation in Python, calculates exposure-aware insurance KPIs, identifies portfolio patterns, and produces Tableau-ready data for an executive dashboard.

---

## Business Problem

Management of a motor-insurance company needs a clear view of the portfolio:
- Where do claims occur most frequently?
- Where are claim costs highest?
- Which policy segments deserve closer attention?
- Which patterns should be monitored in the next reporting cycle?

This is a **descriptive analytics / BI project**, not a pricing or underwriting model. We do not label groups as "high risk" solely based on claim counts — exposure and portfolio size must always be considered.

---

## Dataset

- **Name:** French Motor Third-Party Liability (freMTPL2)
- **Source:** [CASdatasets R Package](https://dutangc.github.io/CASdatasets/reference/freMTPL.html)
- **Policies:** 678,000+ motor third-party liability policies (observed mainly 2011–2013)
- **Claims:** 26,639 individual claim records
- **Original insurer:** Unknown (anonymous dataset)

**Important:** freMTPL2 does **not** include written premium. Therefore, **Loss Ratio must not** be calculated. We use claim frequency, claim severity, and total claim cost as core insurance KPIs.

---

## Data Dictionary

### Frequency Table (freMTPL2freq.csv)

| Variable | Type | Description |
|---|---|---|
| `IDpol` | float | Policy ID (unique identifier) |
| `ClaimNb` | int | Number of claims during exposure period |
| `Exposure` | float | Exposure period in years |
| `VehPower` | int | Vehicle power |
| `VehAge` | int | Vehicle age in years |
| `DrivAge` | int | Driver age in years |
| `BonusMalus` | int | Bonus-malus score (50 = best, 230 = worst) |
| `VehBrand` | str | Vehicle brand category |
| `VehGas` | str | Fuel type (Regular / Diesel) |
| `Area` | str | Density category (A–E) |
| `Density` | int | Population density |
| `Region` | str | French policy region |

### Severity Table (freMTPL2sev.csv)

| Variable | Type | Description |
|---|---|---|
| `IDpol` | int | Policy ID (links to frequency table) |
| `ClaimAmount` | float | Individual claim cost in euros |

---

## KPI Definitions

| KPI | Formula | Explanation |
|---|---|---|
| Policy Count | `count(IDpol)` | Number of unique policies |
| Total Exposure | `sum(Exposure)` | Sum of exposure in years |
| Claim Count | `sum(ClaimNb)` | Total number of claims |
| Claim Frequency | `Claim Count / Exposure` | Claims per exposure year (exposure-adjusted) |
| Total Claim Cost | `sum(ClaimAmount)` | Sum of all claim amounts |
| Avg Claim Severity | `Total Claim Cost / Number of observed claims` | Average cost per observed claim (denominator = row count of severity table, i.e. individual claim records) |

**Note:** Loss Ratio is **not** calculated because written premium is not available in this dataset.

---

## Merge & Cleaning Logic

1. **Frequency table:** 678,013 rows, no duplicates, no missing values
2. **Severity table:** 26,639 rows, aggregated to policy level (sum of ClaimAmount per policy → 24,950 unique policies)
3. **Merge:** Left join from frequency on `IDpol` — all 678,013 policies preserved; severity data filled with 0 for policies without claims
4. **Average Claim Severity:** Computed as `TotalClaimCost / NumIndividualClaims` where `NumIndividualClaims` = row count of the severity table (26,639). This gives average cost **per observed claim**, not per policy. The severity table has one row per individual claim; some policies appear multiple times if they had multiple claims.
5. **Segments engineered:** Driver Age Group, Vehicle Age Group, Vehicle Power Group, Bonus-Malus Category, Density Group
5. **No data deleted:** Zero-exposure rows and negative ClaimNb rows were checked but none found in the clean dataset

---

## Python Analysis Steps

The analysis notebook (`notebooks/analysis.ipynb`) covers:

1. **Data Loading & Inspection** — Load CSVs, check dtypes, shape
2. **Quality Checks & Cleaning** — Missing values, duplicates, negative values, zero exposure
3. **Merge & Feature Engineering** — Aggregate severity to policy level, left merge, create segment bins
4. **Q1: Portfolio Health** — Summary KPIs with interpretation
5. **Q2: Regional Analysis** — Compare regions by frequency, severity, cost/exposure; identify attention area
6. **Q3: Segment Patterns** — Driver age, vehicle age, power, fuel type, bonus-malus comparisons
7. **Q4: Frequency vs Severity** — Scatter/quadrant analysis at segment level
8. **Q5: Pareto Analysis** — Claim cost concentration at individual claim and policy level
9. **Q6: Outlier Investigation** — Extreme claims, unusual combinations, IQR analysis
10. **Q7: Dashboard Design** — Executive dashboard mockup with 3 pages
11. **Q8: Recommendations** — 3 Evidence → Action → KPI recommendations
12. **Tableau Export** — 5 CSV files for Tableau consumption

---

## Tableau Dashboard Structure

### Page 1 — Executive Portfolio Overview
- KPI cards: Policy Count, Exposure, Claim Count, Claim Frequency, Total Claim Cost, Avg Severity
- Horizontal bar: Claim Frequency by Region (with portfolio average)
- Filters: Region, Fuel Type, Density Group

### Page 2 — Claims & Risk Segments
- Driver age vs. claim frequency & severity (dual-axis)
- Vehicle age group comparison
- Frequency vs. Severity scatter (quadrant view)
- Highlight table: Region × Driver Age with claim frequency

### Page 3 — Claim Cost Concentration & Recommendations
- Pareto chart: Cumulative cost by claims
- Top expensive claims table
- Cost distribution by region
- Three business recommendations

---

## Key Findings

1. **Portfolio claim frequency:** 0.1007 claims per exposure year (≈5% of policies generate at least one claim)
2. **Champagne-Ardenne** deserves attention: #1 in both average severity (€3,230) and cost per exposure year (€399)
3. **Young drivers (18–25)** have the highest frequency (0.175) AND highest severity (€4,692)
4. **New vehicles** have very high frequency (0.311) but low severity (€476)
5. **Top 10% of claims** account for ~85%+ of total claim cost (strong Pareto effect)
6. Maximum single claim: €4,075,401 — extreme right-skewed distribution

---

## Three Recommendations

### 1. Target Underwriting Review in High-Frequency Regions
**Evidence:** Champagne-Ardenne has the highest cost per exposure year (€399) and highest average severity (€3,230), with the second-highest claim frequency (0.133).
**Action:** Conduct a focused underwriting review. Examine whether pricing and policy terms adequately reflect observed claim levels.
**KPI:** Monthly claim frequency by region and cost per exposure year.

### 2. Strengthen Monitoring of Young Driver Segment
**Evidence:** Drivers aged 18–25 show claim frequency 0.175 (75% above average) and average severity €4,692 (167% above average).
**Action:** Implement enhanced monitoring. Review whether existing risk differentiation (bonus-malus, vehicle power) adequately captures the observed differential.
**KPI:** Monthly claim frequency and severity for 18–25 group vs. portfolio average.

### 3. Focus Claims Management on High-Cost Tail Claims
**Evidence:** The top 10% of individual claims account for ~85%+ of total claim cost.
**Action:** Establish structured review for claims exceeding the 95th percentile (~€4,862). Investigate for data errors, fraud indicators, and severity patterns.
**KPI:** Monthly count and cost contribution of claims above 95th percentile.

---

## Limitations

1. **Anonymous insurer** — Dataset from an unknown French insurer; findings may not generalise
2. **Historical data** — Mainly 2011–2013; patterns may have changed
3. **No premium data** — Loss Ratio cannot be calculated
4. **Limited features** — Fields do not capture all relevant risk factors
5. **Descriptive only** — Observational associations; causation cannot be established

---

## Repository Structure

```
insurance-claims-dashboard/
├── README.md                                    # This file
├── requirements.txt                             # Python dependencies
├── StudyBuild_DataAnalysisBI_Project01_*.pdf    # Project requirements
├── project_instructions.pdf                     # Project instructions
├── notebooks/
│   └── analysis.ipynb                           # Full analysis notebook (Q1-Q8)
├── data_/
│   ├── README.md                                # Data documentation
│   ├── raw/
│   │   ├── freMTPL2freq.csv                     # Raw frequency data
│   │   └── freMTPL2sev.csv                      # Raw severity data
│   └── processed/
│       ├── tableau_policy_level.csv             # Policy-level data for Tableau
│       ├── tableau_regional_kpi.csv             # Regional KPI summary
│       ├── tableau_segment_analysis.csv         # Segment-level analysis
│       ├── tableau_individual_claims.csv        # Claims for Pareto analysis
│       └── tableau_portfolio_kpi.csv            # Portfolio KPI summary
├── figures/                                     # Matplotlib preview charts (design specs for Tableau)
│   ├── q2_regional_comparison.png               # Regional KPI comparison
│   ├── q3_segment_patterns.png                  # Segment analysis charts
│   ├── q4_frequency_vs_severity.png             # Scatter/quadrant view
│   ├── q5_pareto_analysis.png                   # Pareto cost concentration
│   ├── q6_claim_distribution.png                # Claim amount distribution
│   └── q7_executive_dashboard_preview.png       # Dashboard layout preview
├── report/
│   └── business_summary.md                      # Business summary
└── tableau/                                     # Tableau workbook (build using exported CSVs)
```

---

## How to Reproduce

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd insurance-claims-dashboard
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the analysis notebook:
   ```bash
   jupyter notebook notebooks/analysis.ipynb
   ```

4. The notebook will:
   - Load and clean the raw data
   - Perform all Q1–Q8 analyses
   - Generate matplotlib preview charts in `figures/` (design specifications)
   - Export Tableau-ready CSVs to `data_/processed/`

5. Open the processed CSVs in Tableau Public or Tableau Desktop to build the interactive 3-page dashboard (see Q7 in notebook for chart specifications).

---

## Data Source Citation

> Dutang, C. (2023). CASdatasets: Insurance Datasets. R package.
> https://dutangc.github.io/CASdatasets/reference/freMTPL.html
>
> Boucher, J.-P., & Denuit, M. (2006). Predictive analysis of claim frequencies in motor insurance. Working paper.

---

*StudyBuild — Learn • Build • Apply*
