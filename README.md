# Insurance Claims & Portfolio Risk Analytics — Python + Tableau

**StudyBuild — Project 01 | Data Analysis & Business Intelligence Track**

Author: [Arad Pilevar Javid](https://github.com/AradPilevarJavid)

This project uses the French Motor Third-Party Liability (freMTPL2) dataset to explore insurance claims and portfolio risk patterns. The analysis is mainly done in Python, with Tableau used for the final visual analysis and dashboard.

---

## Business Problem

A motor insurance company needs a clear view of its portfolio:

* Where do claims occur most frequently?
* Where are claim costs highest?
* Which segments show noticeably different claim patterns?
* Which patterns are worth monitoring further?

This is a **descriptive analytics / BI project**, not a pricing or underwriting model. Claim counts alone are not enough to compare groups, so exposure, portfolio size, frequency, and severity are considered together.

---

## Dataset

* **Name:** French Motor Third-Party Liability (freMTPL2)
* **Source:** [CASdatasets R Package](https://dutangc.github.io/CASdatasets/reference/freMTPL.html)
* **Policies:** 678,000+ motor third-party liability policies
* **Claims:** 26,639 individual claim records
* **Original insurer:** Unknown / anonymous dataset

The dataset does **not** contain written premium, so **Loss Ratio is not calculated**. Instead, the analysis focuses on claim frequency, claim severity, and total claim cost.

I went through the project in several main steps. Some of the smaller steps are self-explanatory from the notebook, so I did not document every individual operation here.

1. Data cleaning and quality checks
2. Merging the frequency and severity datasets
3. Feature engineering and segment creation
4. Exploratory data analysis
5. Portfolio and segment analysis
6. Claim-cost concentration and outlier analysis
7. Preparing the data for Tableau
8. Final Tableau dashboard

---

# Report

## Key Findings

1. **Portfolio claim frequency:** 0.1007 claims per exposure year (approximately 5% of policies have at least one claim)
2. **Champagne-Ardenne** shows the highest average severity (€3,230) and cost per exposure year (€399)
3. **Young drivers (18–25)** have the highest observed frequency (0.175) and severity (€4,692)
4. **New vehicles** show very high observed frequency (0.311) but relatively low severity (€476)
5. **The top 10% of individual claims** account for around 60% of total claim cost, while the top 1% account for around 38%
6. The largest observed individual claim is **€4,075,401**, showing the extreme right-skew of claim costs

These findings are descriptive observations from this dataset. They should not be interpreted as evidence that a particular characteristic causes higher claims.

---

## Recommendations

### 1. Review High-Cost Regions

**Evidence:** Champagne-Ardenne has the highest observed average severity (€3,230) and cost per exposure year (€399), while its claim frequency is 0.133.

**Action:** Review the region in more detail and investigate whether the observed severity and cost patterns are consistent across its different policy segments.

**KPI:** Monthly average severity and claim cost per exposure year by region.

### 2. Monitor the Young Driver Segment

**Evidence:** Drivers aged 18–25 have an observed claim frequency of 0.175 and average severity of €4,692.

**Action:** Examine how this segment interacts with other variables such as Bonus-Malus, vehicle power, and vehicle age.

**KPI:** Claim frequency and severity for drivers aged 18–25 compared with the portfolio average.

### 3. Monitor High-Cost Claims

**Evidence:** The largest claims account for a disproportionately large share of total claim cost, with the top 10% contributing around 60%.

**Action:** Pay particular attention to claims in the upper tail of the distribution and investigate unusual or extreme observations.

**KPI:** Number of claims and share of total cost above selected severity thresholds.

---

## Limitations

1. **Anonymous insurer** — The original insurer is not identified, so the results may not generalise to other portfolios.
2. **Historical data** — The dataset is historical, so current insurance patterns may differ.
3. **No premium data** — Loss Ratio cannot be calculated.
4. **Limited features** — The dataset does not contain every factor that could affect insurance claims.
5. **Descriptive analysis** — The observed relationships do not establish causation.
6. **Claim count discrepancy** — `ClaimNb` totals 36,102 claims, while the severity dataset contains 26,639 individual claim records. These two sources do not match perfectly, so I keep their respective definitions separate rather than assuming that every policy-level claim count has a corresponding severity record.

---

## Repository Structure

```text
insurance_final/
├── README.md
├── figures/
│   ├── q2_regional_comparison.png
│   ├── q3_segment_patterns.png
│   ├── q4_frequency_vs_severity.png
│   ├── q5_pareto_analysis.png
│   ├── q6_claim_distribution.png
│   └── q7_executive_dashboard_preview.png
├── notebooks/
│   └── analysis.ipynb
├── report/
│   └── business_summary.md
├── requirements.txt
├── scripts/
│   └── generate_twb.py
└── tableau/
    ├── BUILD_INSTRUCTIONS.md
    └── insurance_claims_dashboard.twb
```

---

## How to Reproduce

Clone the repository and install the required dependencies:

```bash
git clone <repo-url>
cd insurance_final
pip install -r requirements.txt
```

Then run the notebook:

```bash
jupyter notebook notebooks/analysis.ipynb
```

The notebook contains the data cleaning, analysis, visualisations, and Tableau data preparation.

The Tableau files contain the dashboard structure and instructions for rebuilding the final dashboard.

---

## Data Source

> Dutang, C. (2023). CASdatasets: Insurance Datasets. R package.
> https://dutangc.github.io/CASdatasets/reference/freMTPL.html

---

Big thanks to the StudyBuild community for preparing the projects, sharing knowledge, and giving constructive feedback.

If you are interested in joining the community, feel free to message me on [Telegram](https://t.me/nerdysamurai).

*[StudyBuild](https://github.com/StudyBuildCommunity) — Learn • Build • Apply*
