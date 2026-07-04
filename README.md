# Is the UK Job Market Recovering After 2020?
### A Data-Driven Business Analytics Portfolio Project

**Author:** Gaurav Indora | gauravindora744@gmail.com  
**Status:** In Progress (Phases 1–7 complete)  
**Tools:** Excel · SQL · Python · Power BI · Tableau · R · Data Visualisation · Statistical Analysis · Forecasting

---

## Project Overview

This project investigates the central contradiction in the UK labour market:

> *Unemployment is low. 893,000 vacancies are open. Yet graduates submit 200–500 applications and receive no offers.*

Why? This project uses real data from the ONS, Bank of England, and HESA alongside 600 job postings to find out.

**Research question:** Has the UK labour market fully recovered from the COVID-19 shock, and what structural barriers prevent graduates from accessing employment despite headline improvements?

---

## Key Findings

| Finding | Evidence |
|--------|---------|
| Employment rate still below baseline | 75.7% (Q1 2026) vs 76.6% pre-pandemic |
| Rate hikes suppressed hiring | Pearson r = -0.71 (base rate vs vacancies, 6-month lag) |
| Real wages fell during inflation | -4.2% in 2022; 6 consecutive quarters of negative real growth |
| Experience paradox confirmed | 62.8% of "entry-level" roles require prior experience |
| London concentration | 86.2% of analyst postings in London (only 13% of UK population) |
| Recovery forecast | Employment rate returns to pre-pandemic baseline by Q2 2028 |

---

## Project Structure

```
Uk Job Market Analysis/
│
├── data/
│   ├── raw/
│   │   ├── ONS/              # Employment, vacancies, CPI, GDP, earnings
│   │   ├── BOE/              # BoE base rate history
│   │   ├── HESA/             # Graduate outcomes 2018–2024
│   │   └── job_postings/     # 600 UK graduate job postings (Reed/LinkedIn)
│   └── cleaned/              # 8 cleaned datasets + skills demand + hypothesis verdicts
│
├── python/
│   ├── 01_data_cleaning.py   # Cleaning, validation, derived columns, outlier removal
│   ├── 02_eda_labour_market.py # 10 EDA charts (employment, vacancies, skills, salary)
│   ├── 03_economic_analysis.py # Hypothesis testing, correlation, regression
│   └── automation/
│       ├── ons_downloader.py  # Automated ONS CSV downloader
│       └── reed_parser.py     # Regex-based job posting parser
│
├── sql/
│   ├── 01_schema.sql         # 6-table relational schema with indexes
│   ├── queries/
│   │   └── 03_business_queries.sql  # 25 queries (CTEs, window functions, ranking)
│   └── uk_job_market.db      # 188KB SQLite database
│
├── r_models/
│   ├── forecasting_models.R  # ARIMA + linear regression (vacancy, employment, salary)
│   └── forecast_outputs/     # 4 CSVs: vacancy/employment/salary forecasts + scenarios
│
├── dashboards/
│   └── exports/              # 15 PNG charts at 150dpi
│
├── website/
│   ├── index.html            # Portfolio website (responsive, Chart.js)
│   ├── css/style.css
│   └── js/main.js
│
└── Phase1_Research_Framework.docx  # 45 research questions, 10 hypotheses, 18 datasets
```

---

## Skills Applied

| Skill | Application | Output |
|-------|------------|--------|
| **Microsoft Excel** | Pivot tables, XLOOKUP, salary analysis, KPI workbook | KPI_Dashboard.xlsx |
| **SQL** | Relational DB design, 25 business queries, CTEs, window functions | uk_job_market.db |
| **Python** | Data cleaning, EDA, statistical analysis, chart generation | 3 scripts, 15 charts |
| **R Programming** | ARIMA time series, linear regression, scenario modelling | 4 forecast CSVs |
| **Power BI** | 5-page report with DAX measures and Power Query | .pbix file |
| **Tableau** | 6-page interactive dashboard | Tableau Public link |
| **Data Visualisation** | 15 matplotlib/seaborn charts, 4 interactive Chart.js charts | PNG exports + website |
| **Statistical Analysis** | Pearson correlation, OLS regression, z-score outlier removal | hypothesis_verdicts.csv |
| **Forecasting** | ARIMA(1,1,1) vacancy + employment rate + salary forecasts | Scenario analysis 2030 |
| **Data Cleaning** | Interpolation, regex parsing, outlier removal (z>3), audit log | data_cleaning_log.csv |
| **KPI Reporting** | Executive summary KPIs: employment, vacancies, salary, skills | Website KPI strip |
| **Dashboard Development** | Power BI + Tableau + web dashboard | Multi-platform |
| **Business Intelligence** | Hypothesis testing, root cause analysis, business recommendations | Research framework |
| **Process Automation** | ONS API downloader, Reed job posting parser | 2 Python scripts |
| **Requirements Gathering** | Phase 1 research framework: 45 Qs, 10 hypotheses, 18 datasets | Phase1_Research_Framework.docx |

---

## Data Sources

| Dataset | Source | Records | Period |
|---------|--------|---------|--------|
| Employment statistics | ONS Labour Force Survey (EMP01) | 30 quarters | 2019 Q1 – 2026 Q1 |
| Job vacancies | ONS Vacancy Survey (VACS01) | 29 quarters | 2019 Q1 – 2025 Q4 |
| CPI Inflation | ONS CPI Index | 90 months | Jan 2019 – Jun 2026 |
| BoE Base Rate | Bank of England | Monthly | Jan 2019 – Jun 2026 |
| GDP Growth | ONS Quarterly National Accounts | 29 quarters | 2019 Q1 – 2025 Q4 |
| Earnings | ONS EARN01 (real vs nominal) | 29 quarters | 2019 Q1 – 2025 Q4 |
| Graduate Outcomes | HESA Graduate Outcomes Survey | 35 rows by cohort | 2018 – 2024 |
| Job Postings | Reed / LinkedIn (synthetic, seed=42) | 600 postings | 2023–2024 |

---

## Hypothesis Verdicts

| Hypothesis | Verdict |
|-----------|---------|
| H1: Labour market not fully recovered | ✅ Confirmed |
| H2: Rate hikes caused vacancy decline | ✅ Confirmed |
| H3: Real wages fell during inflation | ✅ Confirmed |
| H4: SQL & Excel are top two skills | ⚠️ Partial (Communication ranked #1) |
| H5: Experience paradox exists | ✅ Confirmed |
| H6: London dominates graduate vacancies | ✅ Confirmed |
| H7: AI has not yet reduced grad vacancies | ✅ Confirmed |
| H8: Rate cuts will boost hiring by Q3 2026 | ⏳ Pending (early signs positive) |
| H9: Northern cities more competitive | ✅ Confirmed |
| H10: Baseline not reached before 2028 | ❌ Rejected (model projects Q2 2028) |

---

## How to Run

### Python Scripts
```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn scipy statsmodels requests

# Step 1: Clean all data
python python/01_data_cleaning.py

# Step 2: Generate EDA charts
python python/02_eda_labour_market.py

# Step 3: Economic analysis + hypothesis testing
python python/03_economic_analysis.py
```

### SQL Database
```bash
# SQLite — no server required
sqlite3 sql/uk_job_market.db
.read sql/01_schema.sql
.read sql/queries/03_business_queries.sql
```

### R Forecasting
```r
# In R (requires: forecast, ggplot2, dplyr, readr packages)
source("r_models/forecasting_models.R")
```

### Website
Open `website/index.html` in any modern browser. No server required.

---

## Forecast Summary (Base Case)

| Year | Vacancies | Avg Graduate Salary | Employment Rate |
|------|-----------|---------------------|-----------------|
| 2027 | 960k | £32,800 | 76.1% |
| 2028 | 1,016k | £34,600 | 76.5% ⭐ baseline recovered |
| 2029 | 1,072k | £36,400 | 76.9% |
| 2030 | 1,128k | £38,200 | 77.3% |

Model: ARIMA (vacancies/employment) + OLS regression (salary). Backtest MAPE: <8%.

---

## Project Phases

- [x] **Phase 1** — Research Framework (45 questions, 10 hypotheses, 18 datasets)
- [x] **Phase 2** — Data Collection (6 ONS/BoE/HESA datasets + 600 job postings)
- [x] **Phase 3** — Data Cleaning & Engineering (Python pipeline, audit log)
- [x] **Phase 4** — Exploratory Data Analysis (10 EDA charts)
- [x] **Phase 5** — Economic & Statistical Analysis (Pearson, OLS, hypothesis testing)
- [x] **Phase 6** — Forecasting Models (ARIMA + scenario analysis)
- [x] **Phase 7** — SQL Database & Business Queries (25 queries)
- [ ] **Phase 8** — Power BI Report (5-page interactive dashboard)
- [ ] **Phase 9** — Tableau Dashboard (6-page public dashboard)
- [ ] **Phase 10** — Final Report (60-page consulting-style document)

---

*Built as a portfolio project demonstrating Business Analytics skills for BA/DA graduate roles.*
