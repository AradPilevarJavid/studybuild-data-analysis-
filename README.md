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

**Severity bias caveat:** Average Claim Severity (EUR 2,249) is computed over 26,639 recorded claim amounts; 9,463 policy-level claim counts have no matching severity record. Treat EUR 2,249 as average cost per *reported* claim above the reporting threshold; true average severity across all claim events is likely lower.

---

## Merge & Cleaning Logic

1. **Frequency table:** 678,013 rows, no duplicates, no missing values
2. **Severity table:** 26,639 rows, aggregated to policy level (sum of ClaimAmount per policy → 24,950 unique policies)
3. **Merge:** Left join from frequency on `IDpol` — all 678,013 policies preserved; severity data filled with 0 for policies without claims
4. **Average Claim Severity:** Computed as `TotalClaimCost / NumIndividualClaims` where `NumIndividualClaims` = row count of the severity table (26,639). This gives average cost **per observed claim**, not per policy. The severity table has one row per individual claim; some policies appear multiple times if they had multiple claims.
5. **Segments engineered:** Driver Age Group, Vehicle Age Group, Vehicle Power Group, Bonus-Malus Category, Density Group
6. **No data deleted:** Zero-exposure rows and negative ClaimNb rows were checked but none found in the clean dataset
7. **Claim Count vs. Severity Row Count:** Total Claim Count (36,102) is derived from `sum(ClaimNb)` in the frequency table, which counts the *policy-level claim multiplicity* (a policy with `ClaimNb=3` contributes 3). The severity table contains 26,639 individual claim records — some policies appear multiple times (if they had multiple claims), but not all `ClaimNb` counts necessarily have corresponding severity rows (e.g., claims below reporting thresholds or data entry gaps). This 9,463-row gap is a known limitation of the dataset, not a processing error. Claim Frequency uses `sum(ClaimNb)` as the numerator to remain consistent with the frequency table's own claim accounting.

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
| Chart | What We See | Why It Matters | Decision It Supports |
|---|---|---|---|
| KPI Cards | Portfolio summary: 678K policies, 0.1007 frequency, EUR 2,249 avg severity | Single-glance portfolio health snapshot | Baseline for all subsequent analysis |
| Regional Frequency Bar | Regional variation in claim frequency (0.08–0.14), sorted descending | Identifies which regions have more claims per unit of exposure, controlling for portfolio size | Focus underwriting review on regions above the portfolio average line |
| Regional Cost-per-Exposure Bar | How much each exposure year costs in claims, by region (Champagne-Ardenne leads at EUR 399/yr) | Combines frequency and severity into a single financial metric | Prioritise regions for rate adequacy review |
| Highlight Table | Region × KPI grid showing frequency, severity, and cost-per-exposure | Quick cross-reference of all three regional metrics | Compare regions across multiple dimensions simultaneously |
| **Filters** | Region (multi-select), Fuel Type, Density Group | Allow drill-down by segment | Interactive exploration of sub-portfolios |

### Page 2 — Claims & Risk Segments
| Chart | What We See | Why It Matters | Decision It Supports |
|---|---|---|---|
| Driver Age Frequency Bar | Young drivers (18–25) have the highest frequency (0.175) | 75% above portfolio average — strongest frequency signal | Review risk differentiation for young driver segment |
| Driver Age Severity Bar | Young drivers (18–25) also have the highest severity (EUR 4,692) | 167% above average — strongest combined frequency+severity signal | Enhanced monitoring and possible pricing review |
| Vehicle Age Frequency Bar | New vehicles (age=0) show very high frequency (0.311) but low severity (EUR 476) | Frequency and severity move in opposite directions across vehicle age | Tailor claims handling: rapid settlement for new car minor damage; deeper investigation for old car claims |
| Frequency vs. Severity Scatter | Most regions cluster near the median; Champagne-Ardenne stands out in the high-freq/high-sev quadrant | Identifies regions that are BOTH frequent AND costly vs. one or the other | Quadrant position guides intervention type: frequency reduction vs. severity management |
| Segment Freq vs. Sev Scatter | Segment-level view showing driver age, vehicle age, fuel type, and bonus-malus clusters | Reveals whether high-frequency segments are also high-cost, or cheap-but-frequent | Cross-segment comparison for portfolio prioritisation |

### Page 3 — Claim Cost Concentration & Recommendations
| Chart | What We See | Why It Matters | Decision It Supports |
|---|---|---|---|
| Pareto Chart | Top 1% of claims account for ~38% of total cost; top 10% for ~60% | Cost is extremely concentrated — a small number of high-cost claims dominates financial impact | Establish structured review for claims above the 95th percentile |
| Top Claims Table | Individual claims ranging up to EUR 4M with vehicle and driver characteristics | Allows management to inspect specific high-cost claims for patterns | Investigate individual extreme claims for validity, fraud indicators, or reserving implications |
| Cost Distribution by Region | Absolute cost contribution by region (Ile-de-France and Rhone-Alpes dominate due to portfolio size) | Even moderate-frequency regions can drive significant absolute cost via portfolio volume | Combine with frequency analysis to separate volume effects from genuine risk concentration |
| Three Recommendations | Text summary of Evidence → Action → KPI for each recommendation | Translates data insights into actionable management directives | Direct monthly monitoring and review actions |
| **Dashboard Actions** | Clicking a region in any chart filters all other charts; hover tooltips show detailed KPIs | Enables interactive drill-down | Supports ad-hoc exploration during management meetings |

---

## Key Findings

1. **Portfolio claim frequency:** 0.1007 claims per exposure year (≈5% of policies generate at least one claim)
2. **Champagne-Ardenne** deserves attention: #1 in both average severity (€3,230) and cost per exposure year (€399)
3. **Young drivers (18–25)** have the highest frequency (0.175) AND highest severity (€4,692)
4. **New vehicles** have very high frequency (0.311) but low severity (€476)
5. **Top 10% of claims** account for ~60% of total claim cost (strong Pareto effect); top 1% alone accounts for ~38%
6. Maximum single claim: €4,075,401 — extreme right-skewed distribution

---

## Three Recommendations

### 1. Target Underwriting Review in High-Cost Regions
**Evidence:** Champagne-Ardenne ranks #1 in both average severity (€3,230) and cost per exposure year (€399), despite being #2 in claim frequency (0.133, behind Corse at 0.143). Its real signal is severity and cost, not frequency alone.
**Action:** Conduct a focused underwriting review in Champagne-Ardenne. Examine whether pricing and policy terms adequately reflect the observed severity and cost-per-exposure levels.
**KPI:** Monthly average severity and cost per exposure year by region.

### 2. Strengthen Monitoring of Young Driver Segment
**Evidence:** Drivers aged 18–25 show claim frequency 0.175 (75% above average) and average severity €4,692 (167% above average).
**Action:** Implement enhanced monitoring. Review whether existing risk differentiation (bonus-malus, vehicle power) adequately captures the observed differential.
**KPI:** Monthly claim frequency and severity for 18–25 group vs. portfolio average.

### 3. Focus Claims Management on High-Cost Tail Claims
**Evidence:** The top 10% of individual claims account for ~60% of total claim cost (top 1% alone accounts for ~38%).
**Action:** Establish structured review for claims exceeding the 95th percentile (~€4,862). Investigate for data errors, fraud indicators, and severity patterns.
**KPI:** Monthly count and cost contribution of claims above 95th percentile.

---

## Limitations

1. **Anonymous insurer** — Dataset from an unknown French insurer; findings may not generalise
2. **Historical data** — Mainly 2011–2013; patterns may have changed
3. **No premium data** — Loss Ratio cannot be calculated
4. **Limited features** — Fields do not capture all relevant risk factors
5. **Descriptive only** — Observational associations; causation cannot be established
6. **Claim count discrepancy** — Total Claim Count (36,102 from `sum(ClaimNb)`) exceeds severity table rows (26,639) by 9,463. The frequency table counts claim multiplicity at the policy level; the severity table records individual claims with amounts. Not all policy-level claim counts have matching severity records (possible causes: sub-threshold claims, reporting gaps, or data entry issues). This gap does not affect Claim Frequency or Average Claim Severity calculations, which use their respective denominators correctly.

---

## Repository Structure

```
insurance-claims-dashboard/
├── README.md
├── requirements.txt                          
├── StudyBuild_DataAnalysisBI_Project01_*.pdf  
├── project_instructions.pdf                  
├── notebooks/
│   └── analysis.ipynb     
├── data/
│   ├── README.md  
│   ├── raw/
│   │   ├── freMTPL2freq.csv                  
│   │   └── freMTPL2sev.csv                    
│   └── processed/
│       ├── tableau_policy_level.csv           
│       ├── tableau_regional_kpi.csv          
│       ├── tableau_segment_analysis.csv        
│       ├── tableau_individual_claims.csv       
│       └── tableau_portfolio_kpi.csv           
├── figures/                                  
│   ├── q2_regional_comparison.png             
│   ├── q3_segment_patterns.png               
│   ├── q4_frequency_vs_severity.png           
│   ├── q5_pareto_analysis.png                 
│   ├── q6_claim_distribution.png               
│   └── q7_executive_dashboard_preview.png    
├── report/
│   └── business_summary.md                     
└── tableau/
    ├── insurance_claims_dashboard.twb      
    └── BUILD_INSTRUCTIONS.md                  
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
   - Export Tableau-ready CSVs to `data/processed/`

5. Open the Tableau workbook:
   ```bash
   tableau/BUILD_INSTRUCTIONS.md
   ```
   Follow `tableau/BUILD_INSTRUCTIONS.md` for step-by-step instructions to build
   the 3-page dashboard in Tableau Desktop or Tableau Public:
   - **Page 1:** Executive Portfolio Overview (KPI cards, regional bar charts, highlight table, filters)
   - **Page 2:** Claims & Risk Segments (driver/vehicle bars, frequency-vs-severity scatter, segment scatter)
   - **Page 3:** Claim Cost Concentration (dual-axis Pareto bars+line, top claims table, cost distribution, recommendations text zone)

   The `.twb` file is a schema scaffold only (declares datasources and field names)
   and will open as blank worksheets. Build the real dashboard from the CSVs using
   the instructions, then save as `.twbx`.

---

## Data Source Citation

> Dutang, C. (2023). CASdatasets: Insurance Datasets. R package.
> https://dutangc.github.io/CASdatasets/reference/freMTPL.html
>
> Boucher, J.-P., & Denuit, M. (2006). Predictive analysis of claim frequencies in motor insurance. Working paper.

---

*StudyBuild — Learn • Build • Apply*
