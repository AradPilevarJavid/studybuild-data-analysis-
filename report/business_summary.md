# Insurance Claims & Portfolio Risk Analytics — Business Summary

## Dataset
- **Source:** French Motor Third-Party Liability (freMTPL2) — CASdatasets
- **URL:** https://dutangc.github.io/CASdatasets/reference/freMTPL.html
- **Policies:** 678,000+ motor third-party liability policies (observed 2011–2013)
- **Claims:** 26,639 individual claim records
- **Note:** Written premium is not available in this dataset. Loss Ratio cannot be calculated.

---

## Portfolio Health Summary

| KPI | Value |
|---|---|
| Policy Count | 678,013 |
| Total Exposure | 358,499 years |
| Total Claim Count | 36,102 |
| Policies with Claims | 34,060 (5.0%) |
| Claim Frequency | 0.1007 (per exposure year) |
| Total Claim Cost | €59,909,216 |
| Average Claim Severity | €1,759 (per policy with claims) |
| Cost per Exposure Year | €167 |

**Why raw claim counts are misleading:** A region or segment with more policies and/or longer exposure naturally accumulates more claims even if the underlying risk profile is identical. Claim frequency (claims per unit of exposure) normalises for this and enables fair comparison.

---

## Key Findings

### Q2 — Regional Claim Burden
- **Champagne-Ardenne** deserves attention: it ranks **#1 in average severity (€3,230)** and **#1 in cost per exposure year (€399)**, while also having the second-highest claim frequency (0.133).
- **Corse** has the highest claim frequency (0.143) but moderate severity, suggesting a high-frequency, lower-severity pattern.
- **Île-de-France** contributes the largest absolute cost (€4.6M) due to its large portfolio, but its frequency is only slightly above average.

### Q3 — Driver & Vehicle Segment Patterns
- **Young drivers (18–25)** have the highest claim frequency (0.175) **and** the highest average severity (€4,692). This is the strongest pattern in the data.
- **New vehicles (VehAge = 0)** show a very high frequency (0.311) but low severity (€476), suggesting many small/low-cost claims on new cars.
- **Old vehicles (11+)** have the lowest frequency (0.080) but higher severity (€2,607), indicating that when older vehicles do claim, the damage tends to be more costly.
- **Bonus-Malus** strongly correlates with frequency: drivers with scores above 100 claim at roughly 3× the rate of those at 50 (best).

### Q4 — Frequency vs. Severity
- The scatter plot of regional frequency vs. severity reveals that **most regions cluster around the portfolio average**. Champagne-Ardenne stands out in the high-frequency / high-severity quadrant.
- High frequency does **not** automatically imply high severity — these are distinct dimensions that must be evaluated independently.

### Q5 — Claim Cost Concentration (Pareto)
- The **top 10% of individual claims** account for approximately **85%+ of total claim cost**.
- The **top 1% of claims** alone account for a very large share of total cost.
- This extreme concentration means that focused review of the most expensive claims can have an outsized impact on portfolio performance.

### Q6 — Unusual Claims
- The maximum single claim amount is **€4,075,401** — more than 1,800× the median claim (€1,172).
- The 99.9th percentile is €162,784, indicating a very long right tail.
- **Young drivers with powerful vehicles (age ≤ 25, power ≥ 10)** form an unusual segment that should be investigated, even though it is small in absolute terms.
- These extreme values should **not** be deleted automatically. Insurance claim distributions are inherently skewed; the business must understand and manage the tail risk.

---

## Three Data-Driven Recommendations

### Recommendation 1: Target Underwriting Review in High-Frequency Regions

| | |
|---|---|
| **Evidence** | Champagne-Ardenne has the highest cost per exposure year (€399) and the highest average severity (€3,230), combined with the second-highest claim frequency (0.133). Corse has the highest claim frequency (0.143). |
| **Action** | Conduct a focused underwriting review in these regions. Examine whether current pricing and policy terms adequately reflect the observed claim frequency and severity levels. Consider whether the region-level portfolio mix is optimal. |
| **KPI** | Track monthly claim frequency by region and cost per exposure year. |

### Recommendation 2: Strengthen Monitoring of Young Driver Segment

| | |
|---|---|
| **Evidence** | Drivers aged 18–25 show a claim frequency of 0.175 (75% above portfolio average) and an average severity of €4,692 (167% above portfolio average). This is the segment with the strongest combined frequency-severity signal. |
| **Action** | Implement enhanced monitoring of the young driver portfolio segment. Review whether existing risk differentiation (bonus-malus, vehicle power restrictions) adequately captures the frequency and severity differential observed in the data. |
| **KPI** | Monthly claim frequency and average severity for the 18–25 age group versus portfolio average. |

### Recommendation 3: Focus Claims Management on High-Cost Tail Claims

| | |
|---|---|
| **Evidence** | The top 10% of individual claims account for approximately 85%+ of total claim cost. The top 1% alone represent a disproportionate share. This extreme concentration means a small number of high-cost claims has outsized financial impact. |
| **Action** | Establish a structured review process for claims exceeding the 95th percentile of claim amounts (approximately €4,862). Investigate these claims for data entry errors, fraud indicators, and severity patterns that could inform reserving and pricing decisions. |
| **KPI** | Monthly monitoring of claims above the 95th percentile threshold — tracking both count and total cost contribution. |

---

## Limitations

1. **Anonymous insurer:** The dataset comes from an unknown private French insurer. Findings may not generalise to other markets or time periods.
2. **Historical data:** The data mainly covers 2011–2013. Patterns may have changed.
3. **No premium data:** Loss Ratio cannot be calculated. We rely on frequency, severity, and total cost as core KPIs.
4. **Limited features:** The available fields (vehicle power, age, bonus-malus, region) do not capture every factor relevant to insurance risk (e.g., driver behaviour, telematics, weather, road conditions).
5. **Descriptive only:** All findings are observational associations. We cannot establish causation from this data alone.

---

## How to Reproduce

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run `jupyter notebook notebooks/analysis.ipynb`
4. The notebook will generate all analysis figures in `figures/` and Tableau-ready CSV files in `data_/processed/`
5. Open the CSV files in Tableau Public/Desktop to build the dashboard

---

*StudyBuild — Learn • Build • Apply*
