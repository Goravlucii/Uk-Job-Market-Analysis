"""
UK Job Market Analysis — Script 01: Data Cleaning & Transformation
Author: Gaurav Indora
Purpose: Load all raw datasets, clean, validate, merge, and output analysis-ready CSVs.
Skills demonstrated: Python, Pandas, Data Cleaning, Process Automation
"""

import pandas as pd
import numpy as np
import os, re, warnings
from datetime import datetime

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(ROOT, "data", "raw")
CLEAN = os.path.join(ROOT, "data", "cleaned")
os.makedirs(CLEAN, exist_ok=True)

log_rows = []

def log(dataset, action, before, after, notes=""):
    log_rows.append({"dataset":dataset,"action":action,"rows_before":before,"rows_after":after,"notes":notes,"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    print(f"  [{dataset}] {action}: {before} → {after} rows. {notes}")

print("=" * 65)
print("UK JOB MARKET ANALYSIS — DATA CLEANING PIPELINE")
print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 65)

# ─────────────────────────────────────────────────────────────────────────────
# 1. EMPLOYMENT DATA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/6] Cleaning Employment Data...")
emp = pd.read_csv(f"{RAW}/ONS/employment.csv")
n0 = len(emp)
emp["period_dt"] = pd.to_datetime(emp["year"].astype(str) + "-" + emp["quarter"].str[-1].astype(str).map({"1":"01","2":"04","3":"07","4":"10"}), format="%Y-%m")
emp["employment_gap_vs_2019"] = emp["employment_rate_pct"] - 76.6  # vs Q4 2019 baseline
emp["unemployment_gap_vs_2019"] = emp["unemployment_rate_pct"] - 3.9
emp["real_employed_millions"] = (emp["employed_thousands"] / 1000).round(2)
emp = emp.dropna(subset=["employment_rate_pct","unemployment_rate_pct"])
log("Employment", "Clean + feature engineer", n0, len(emp), "Added period_dt, gap_vs_2019 cols")
emp.to_csv(f"{CLEAN}/employment_clean.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 2. VACANCIES DATA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/6] Cleaning Vacancies Data...")
vac = pd.read_csv(f"{RAW}/ONS/vacancies.csv")
n0 = len(vac)
vac["period_dt"] = pd.to_datetime(vac["year"].astype(str) + "-" + vac["quarter"].str[-1].astype(str).map({"1":"01","2":"04","3":"07","4":"10"}), format="%Y-%m")
vac["vacancies_vs_peak_pct"] = ((vac["total_vacancies_thousands"] / 1295) * 100).round(1)
vac["vacancies_vs_prepandemic_pct"] = ((vac["total_vacancies_thousands"] / 820) * 100).round(1)
vac["qoq_change_thousands"] = vac["total_vacancies_thousands"].diff().round(1)
vac["qoq_change_pct"] = (vac["total_vacancies_thousands"].pct_change() * 100).round(2)
log("Vacancies", "Clean + derive metrics", n0, len(vac), "Added vs_peak, vs_prepandemic, qoq_change")
vac.to_csv(f"{CLEAN}/vacancies_clean.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 3. CPI + BOE RATE MERGE
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3/6] Cleaning & Merging CPI + BoE Rate...")
cpi = pd.read_csv(f"{RAW}/ONS/cpi_inflation.csv")
boe = pd.read_csv(f"{RAW}/BOE/base_rate.csv")
n0 = len(cpi)
cpi["period_dt"] = pd.to_datetime(cpi["period"])
boe["period_dt"] = pd.to_datetime(boe["period"])
economic = cpi.merge(boe[["period","base_rate_pct"]], on="period", how="left")
economic["real_rate"] = economic["base_rate_pct"] - economic["cpi_pct"]
economic["rate_inflation_gap"] = (economic["base_rate_pct"] - economic["cpi_pct"]).round(2)
economic["inflation_target_miss"] = (economic["cpi_pct"] - 2.0).round(2)
economic["rolling_3m_avg_cpi"] = economic["cpi_pct"].rolling(3).mean().round(2)
log("CPI+BoE", "Merge + calculate real rate", n0, len(economic), "Added real_rate, rolling avg, target miss")
economic.to_csv(f"{CLEAN}/economic_indicators_clean.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 4. GDP DATA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/6] Cleaning GDP Data...")
gdp = pd.read_csv(f"{RAW}/ONS/gdp.csv")
n0 = len(gdp)
gdp["period_dt"] = pd.to_datetime(gdp["year"].astype(str) + "-" + gdp["quarter"].str[-1].astype(str).map({"1":"01","2":"04","3":"07","4":"10"}), format="%Y-%m")
gdp["cumulative_growth_vs_2019Q4"] = ((gdp["gdp_gbp_billions"] / 2221.7 - 1) * 100).round(2)
gdp["rolling_annual_growth"] = gdp["gdp_growth_pct"].rolling(4).sum().round(2)
gdp["recession_indicator"] = ((gdp["gdp_growth_pct"] < 0) & (gdp["gdp_growth_pct"].shift(1) < 0)).astype(int)
log("GDP", "Clean + derive cumulative + recession flag", n0, len(gdp), "Added cumulative_growth, recession_indicator")
gdp.to_csv(f"{CLEAN}/gdp_clean.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 5. MASTER LABOUR MARKET TABLE (quarterly merge)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5/6] Building Master Labour Market Dataset...")
master = emp[["period","year","quarter","employment_rate_pct","unemployment_rate_pct",
              "inactivity_rate_pct","employed_thousands","employment_gap_vs_2019"]].copy()
master = master.merge(vac[["period","total_vacancies_thousands","vacancies_vs_prepandemic_pct","qoq_change_pct"]], on="period", how="left")
master = master.merge(gdp[["period","gdp_growth_pct","gdp_gbp_billions","recession_indicator"]], on="period", how="left")

# Add quarterly average CPI and BoE rate
cpi_q = economic.groupby(["year","month"])["cpi_pct"].mean().reset_index()
economic["year"] = economic["period_dt"].dt.year
economic["quarter"] = economic["period_dt"].dt.month.map({1:"Q1",2:"Q1",3:"Q1",4:"Q2",5:"Q2",6:"Q2",7:"Q3",8:"Q3",9:"Q3",10:"Q4",11:"Q4",12:"Q4"})
eco_q = economic.groupby(["year","quarter"]).agg(avg_cpi_pct=("cpi_pct","mean"),avg_base_rate_pct=("base_rate_pct","mean")).reset_index()
eco_q["period"] = eco_q["year"].astype(str) + eco_q["quarter"]
master = master.merge(eco_q[["period","avg_cpi_pct","avg_base_rate_pct"]], on="period", how="left")
master["avg_cpi_pct"] = master["avg_cpi_pct"].round(2)
master["avg_base_rate_pct"] = master["avg_base_rate_pct"].round(2)

n0=len(master)
log("Master", "Quarterly merge: employment + vacancies + GDP + CPI + rates", n0, len(master), "Master table ready")
master.to_csv(f"{CLEAN}/master_labour_market.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 6. JOB POSTINGS DATA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[6/6] Cleaning Job Postings Data...")
jobs = pd.read_csv(f"{RAW}/job_postings/reed_postings.csv")
n0 = len(jobs)

# Standardise salary columns
jobs["salary_min_gbp"] = pd.to_numeric(jobs["salary_min_gbp"], errors="coerce")
jobs["salary_max_gbp"] = pd.to_numeric(jobs["salary_max_gbp"], errors="coerce")
jobs["salary_midpoint"] = ((jobs["salary_min_gbp"] + jobs["salary_max_gbp"]) / 2).round(0)
jobs["has_salary"] = jobs["salary_min_gbp"].notna()
jobs["date_posted"] = pd.to_datetime(jobs["date_posted"], format="%Y-%m")

# Standardise experience required
exp_map = {"None":"No experience required","0-1 years":"<1 year","1 year":"1 year","1-2 years":"1-2 years","2 years":"2+ years"}
jobs["experience_required"] = jobs["experience_required"].map(exp_map).fillna(jobs["experience_required"])
jobs["requires_experience"] = jobs["experience_required"].isin(["1 year","1-2 years","2+ years"]).astype(int)

# London flag
jobs["is_london"] = (jobs["city"] == "London").astype(int)

# Skills explosion: count skills per posting
jobs["skills_list"] = jobs["skills_required"].str.split(";")
jobs["skill_count"] = jobs["skills_list"].apply(lambda x: len(x) if isinstance(x,list) else 0)

# Remove outliers (salary z-score)
sal_mean = jobs["salary_midpoint"].mean()
sal_std  = jobs["salary_midpoint"].std()
jobs["salary_zscore"] = ((jobs["salary_midpoint"] - sal_mean) / sal_std).round(2)
n1 = len(jobs)
jobs = jobs[jobs["salary_zscore"].abs() < 3]
log("JobPostings", "Clean, standardise, flag outliers", n0, len(jobs), f"Removed {n1-len(jobs)} salary outliers (z>3)")

jobs.to_csv(f"{CLEAN}/graduate_jobs_clean.csv", index=False)

# Skills demand table
all_skills = []
for _, row in jobs.iterrows():
    if isinstance(row["skills_list"], list):
        for s in row["skills_list"]:
            s=s.strip()
            if s: all_skills.append({"skill":s,"sector":row["sector"],"city":row["city"],"year":row["date_posted"].year if pd.notna(row["date_posted"]) else None})

skills_df = pd.DataFrame(all_skills)
skill_counts = skills_df.groupby("skill").size().reset_index(name="frequency")
skill_counts["pct_of_postings"] = (skill_counts["frequency"] / len(jobs) * 100).round(1)
skill_counts = skill_counts.sort_values("frequency", ascending=False).reset_index(drop=True)
skill_counts["rank"] = skill_counts.index + 1
skill_counts.to_csv(f"{CLEAN}/skills_demand.csv", index=False)

log("Skills", "Extract skill frequency rankings", len(all_skills), len(skill_counts), "skills_demand.csv created")

# ─────────────────────────────────────────────────────────────────────────────
# CLEANING LOG
# ─────────────────────────────────────────────────────────────────────────────
log_df = pd.DataFrame(log_rows)
log_df.to_csv(f"{CLEAN}/data_cleaning_log.csv", index=False)

print("\n" + "=" * 65)
print("DATA CLEANING COMPLETE")
print(f"Outputs saved to: data/cleaned/")
print(f"Log saved to: data/cleaned/data_cleaning_log.csv")
print("=" * 65)
print("\nFiles created:")
for f in sorted(os.listdir(CLEAN)): print(f"  ✓ {f}")
