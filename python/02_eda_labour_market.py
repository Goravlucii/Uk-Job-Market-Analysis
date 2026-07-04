"""
UK Job Market Analysis — Script 02: Exploratory Data Analysis
Author: Gaurav Indora
Purpose: Answer research questions Groups A-C through visualisation & statistics.
Skills demonstrated: Python, Statistical Analysis, Data Visualisation, Excel-equivalent analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mtick
import warnings, os
from scipy import stats

warnings.filterwarnings("ignore")
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.spines.top":False,"axes.spines.right":False})

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT,"data","cleaned")
EXPORTS = os.path.join(ROOT,"dashboards","exports")
os.makedirs(EXPORTS, exist_ok=True)

NAVY="#1B3A6B"; BLUE="#2563A8"; RED="#B91C1C"; GREEN="#166534"; AMBER="#D97706"; LGRAY="#F3F6FB"

print("="*65)
print("UK JOB MARKET ANALYSIS — EXPLORATORY DATA ANALYSIS")
print("="*65)

emp = pd.read_csv(f"{CLEAN}/employment_clean.csv")
vac = pd.read_csv(f"{CLEAN}/vacancies_clean.csv")
eco = pd.read_csv(f"{CLEAN}/economic_indicators_clean.csv")
gdp = pd.read_csv(f"{CLEAN}/gdp_clean.csv")
master = pd.read_csv(f"{CLEAN}/master_labour_market.csv")
jobs = pd.read_csv(f"{CLEAN}/graduate_jobs_clean.csv")
skills = pd.read_csv(f"{CLEAN}/skills_demand.csv")

# ── CHART 1: Employment Rate 2019-2026 with baseline ─────────────────────────
print("\n[Chart 1] Employment Rate Trend...")
fig, ax = plt.subplots(figsize=(13,5.5))
ax.axhline(76.6, color=GREEN, linestyle="--", lw=1.5, label="Pre-pandemic baseline (76.6%)")
ax.axhspan(74.0, 75.2, alpha=0.08, color=RED, label="COVID impact zone")
ax.plot(range(len(emp)), emp["employment_rate_pct"], color=NAVY, lw=2.5, marker="o", ms=4, zorder=5)
ax.fill_between(range(len(emp)), emp["employment_rate_pct"], 73.5, alpha=0.08, color=BLUE)
ax.annotate("COVID crash\n-2.2pp", xy=(4,74.4), xytext=(6,73.8), arrowprops=dict(arrowstyle="->",color=RED), color=RED, fontsize=9)
ax.annotate("Still below\nbaseline (2026)", xy=(len(emp)-1,75.7), xytext=(len(emp)-4,74.9), arrowprops=dict(arrowstyle="->",color=AMBER), color=AMBER, fontsize=9)
ax.set_xticks(range(0,len(emp),2)); ax.set_xticklabels(emp["period"][::2], rotation=45, ha="right", fontsize=8)
ax.set_ylim(73,78); ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
ax.set_title("UK Employment Rate (16-64, Seasonally Adjusted) 2019–2026", fontsize=14, fontweight="bold", color=NAVY, pad=15)
ax.set_ylabel("Employment Rate (%)"); ax.legend(fontsize=9)
ax.text(0.01,0.02,"Source: ONS Labour Force Survey (EMP01)  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/01_employment_rate_trend.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 01_employment_rate_trend.png")

# ── CHART 2: Unemployment Rate with COVID peak ────────────────────────────────
print("[Chart 2] Unemployment Rate...")
fig, ax = plt.subplots(figsize=(13,5.5))
ax.axhline(3.9, color=GREEN, linestyle="--", lw=1.5, label="Pre-pandemic baseline (3.9%)")
ax.fill_between(range(len(emp)), emp["unemployment_rate_pct"], 3.5, where=emp["unemployment_rate_pct"]>3.9, alpha=0.18, color=RED, label="Above pre-pandemic level")
ax.plot(range(len(emp)), emp["unemployment_rate_pct"], color=RED, lw=2.5, marker="o", ms=4)
ax.annotate(f"Peak: 5.0%\n(Q4 2020)", xy=(4,5.0), xytext=(8,5.2), arrowprops=dict(arrowstyle="->",color=RED), color=RED, fontsize=9)
ax.annotate(f"Low: 3.5%\n(Q3 2022)", xy=(15,3.5), xytext=(12,3.2), arrowprops=dict(arrowstyle="->",color=GREEN), color=GREEN, fontsize=9)
ax.set_xticks(range(0,len(emp),2)); ax.set_xticklabels(emp["period"][::2], rotation=45, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
ax.set_title("UK Unemployment Rate 2019–2026", fontsize=14, fontweight="bold", color=NAVY, pad=15)
ax.set_ylabel("Unemployment Rate (%)"); ax.legend(fontsize=9)
ax.text(0.01,0.02,"Source: ONS Labour Force Survey  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/02_unemployment_rate.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 02_unemployment_rate.png")

# ── CHART 3: UK Vacancies – full cycle ───────────────────────────────────────
print("[Chart 3] Vacancy Cycle...")
fig, ax = plt.subplots(figsize=(13,5.5))
ax.axhline(820, color=GREEN, linestyle="--", lw=1.5, alpha=0.7, label="Pre-pandemic level (~820k)")
ax.fill_between(range(len(vac)), vac["total_vacancies_thousands"], 400, alpha=0.12, color=BLUE)
ax.plot(range(len(vac)), vac["total_vacancies_thousands"], color=BLUE, lw=2.5, marker="o", ms=4)
peak_idx = vac["total_vacancies_thousands"].idxmax()
ax.annotate("RECORD PEAK\n1,295k (Q2 2022)", xy=(peak_idx-1,1295), xytext=(peak_idx-5,1350), arrowprops=dict(arrowstyle="->",color=NAVY), color=NAVY, fontsize=9, fontweight="bold")
ax.annotate("COVID crash\n476k (Q2 2020)", xy=(5,476), xytext=(8,380), arrowprops=dict(arrowstyle="->",color=RED), color=RED, fontsize=9)
ax.set_xticks(range(0,len(vac),2)); ax.set_xticklabels(vac["period"][::2], rotation=45, ha="right", fontsize=8)
ax.set_title("UK Total Job Vacancies (Thousands) 2019–2026", fontsize=14, fontweight="bold", color=NAVY, pad=15)
ax.set_ylabel("Vacancies (Thousands)"); ax.legend(fontsize=9)
ax.text(0.01,0.02,"Source: ONS Vacancy Survey (VACS01)  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/03_vacancies_trend.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 03_vacancies_trend.png")

# ── CHART 4: CPI Inflation ────────────────────────────────────────────────────
print("[Chart 4] CPI Inflation...")
eco["period_dt"] = pd.to_datetime(eco["period"])
fig, ax = plt.subplots(figsize=(13,5.5))
ax.axhline(2.0, color=GREEN, linestyle="--", lw=1.5, label="BoE 2% target")
ax.fill_between(eco.index, eco["cpi_pct"], 2.0, where=eco["cpi_pct"]>2.0, alpha=0.2, color=RED, label="Above target")
ax.fill_between(eco.index, eco["cpi_pct"], 2.0, where=eco["cpi_pct"]<2.0, alpha=0.2, color=GREEN, label="Below target")
ax.plot(eco.index, eco["cpi_pct"], color=RED, lw=2, label="CPI %")
peak_i = eco["cpi_pct"].idxmax()
ax.annotate(f"PEAK: 11.1%\nOct 2022", xy=(peak_i,11.1), xytext=(peak_i-12,10.0), arrowprops=dict(arrowstyle="->",color=RED), color=RED, fontsize=9, fontweight="bold")
tick_idx = list(range(0,len(eco),6))
ax.set_xticks(tick_idx); ax.set_xticklabels(eco["period"].iloc[tick_idx], rotation=45, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
ax.set_title("UK CPI Inflation Rate 2019–2026 vs Bank of England 2% Target", fontsize=14, fontweight="bold", color=NAVY, pad=15)
ax.set_ylabel("CPI (%)"); ax.legend(fontsize=9)
ax.text(0.01,0.02,"Source: ONS / Bank of England  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/04_cpi_inflation.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 04_cpi_inflation.png")

# ── CHART 5: BoE Base Rate vs Vacancies (dual axis) ──────────────────────────
print("[Chart 5] Base Rate vs Vacancies...")
fig, ax1 = plt.subplots(figsize=(13,5.5))
ax2 = ax1.twinx()
# Quarterly averages of base rate
master_plot = master.dropna(subset=["avg_base_rate_pct","total_vacancies_thousands"])
x = range(len(master_plot))
ax1.plot(x, master_plot["total_vacancies_thousands"], color=BLUE, lw=2.5, label="Vacancies (000s)")
ax1.fill_between(x, master_plot["total_vacancies_thousands"], 400, alpha=0.1, color=BLUE)
ax2.plot(x, master_plot["avg_base_rate_pct"], color=RED, lw=2.5, linestyle="--", label="BoE Base Rate %")
ax1.set_ylabel("Vacancies (Thousands)", color=BLUE)
ax2.set_ylabel("BoE Base Rate (%)", color=RED)
ax1.set_xticks(range(0,len(master_plot),2)); ax1.set_xticklabels(master_plot["period"][::2].values, rotation=45, ha="right", fontsize=8)
lines1,l1 = ax1.get_legend_handles_labels(); lines2,l2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2,l1+l2,fontsize=9,loc="upper right")
ax1.set_title("UK Job Vacancies vs Bank of England Base Rate 2020–2026\n(Inverse relationship: as rates rise, vacancies fall)", fontsize=13, fontweight="bold", color=NAVY, pad=15)
ax1.text(0.01,0.02,"Source: ONS VACS01 + Bank of England  |  Gaurav Indora, 2026",transform=ax1.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/05_rate_vs_vacancies.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 05_rate_vs_vacancies.png")

# ── CHART 6: GDP Growth ───────────────────────────────────────────────────────
print("[Chart 6] GDP Growth...")
fig, ax = plt.subplots(figsize=(13,5.5))
colors = [RED if g<0 else BLUE for g in gdp["gdp_growth_pct"]]
bars = ax.bar(range(len(gdp)), gdp["gdp_growth_pct"], color=colors, width=0.7, zorder=3)
ax.axhline(0, color="black", lw=0.8)
ax.axhline(gdp[gdp["year"]<=2019]["gdp_growth_pct"].mean(), color=GREEN, linestyle="--", lw=1.5, label=f"Pre-pandemic avg")
min_i = gdp["gdp_growth_pct"].idxmin()
ax.annotate(f"-19.8%\nQ2 2020", xy=(min_i,-19.8), xytext=(min_i+2,-16), arrowprops=dict(arrowstyle="->",color=RED), color=RED, fontsize=9, fontweight="bold")
ax.set_xticks(range(0,len(gdp),2)); ax.set_xticklabels(gdp["period"][::2], rotation=45, ha="right", fontsize=8)
ax.set_title("UK GDP Quarterly Growth Rate 2019–2026 (%)", fontsize=14, fontweight="bold", color=NAVY, pad=15)
ax.set_ylabel("GDP Growth (%)"); ax.legend(fontsize=9); ax.grid(axis="y", alpha=0.3, zorder=0)
ax.text(0.01,0.02,"Source: ONS National Accounts  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/06_gdp_growth.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 06_gdp_growth.png")

# ── CHART 7: Top 15 Skills Demand ─────────────────────────────────────────────
print("[Chart 7] Skills Demand Ranking...")
top15 = skills.head(15).sort_values("frequency")
fig, ax = plt.subplots(figsize=(11,7))
bar_colors = [RED if s in ["SQL","Python","Power BI","Tableau","R Programming"] else BLUE for s in top15["skill"]]
bars = ax.barh(top15["skill"], top15["pct_of_postings"], color=bar_colors, height=0.65)
for bar, pct in zip(bars, top15["pct_of_postings"]):
    ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2, f"{pct:.1f}%", va="center", fontsize=9, color=NAVY, fontweight="bold")
tech_patch = mpatches.Patch(color=RED, label="Technical / Tool skills")
soft_patch = mpatches.Patch(color=BLUE, label="Business / Soft skills")
ax.legend(handles=[tech_patch,soft_patch], fontsize=9)
ax.set_xlim(0,105); ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_title("Top 15 Skills in UK Graduate Analyst Job Postings 2024–2026\n(% of 600 postings analysed)", fontsize=13, fontweight="bold", color=NAVY, pad=15)
ax.set_xlabel("% of Job Postings")
ax.text(0.01,-0.08,"Source: Reed & LinkedIn job posting analysis — 600 postings  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/07_skills_demand.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 07_skills_demand.png")

# ── CHART 8: Salary by City ────────────────────────────────────────────────────
print("[Chart 8] Salary by City...")
city_salary = jobs[jobs["salary_midpoint"].notna()].groupby("city")["salary_midpoint"].agg(["mean","median","count"]).reset_index()
city_salary.columns = ["city","mean_salary","median_salary","count"]
city_salary = city_salary[city_salary["count"]>=8].sort_values("median_salary",ascending=True)
fig, ax = plt.subplots(figsize=(11,6))
bars = ax.barh(city_salary["city"], city_salary["median_salary"]/1000, color=[RED if c=="London" else BLUE for c in city_salary["city"]], height=0.6)
for bar, val, n in zip(bars, city_salary["median_salary"], city_salary["count"]):
    ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2, f"£{val/1000:.1f}k  (n={n})", va="center", fontsize=9.5)
ax.set_xlim(0, city_salary["median_salary"].max()/1000 + 8)
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"£{x:.0f}k"))
ax.set_title("Median Graduate Analyst Salary by UK City (2024–2026)", fontsize=13, fontweight="bold", color=NAVY, pad=15)
ax.text(0.01,-0.09,"Source: Reed job postings (postings with disclosed salary only)  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/08_salary_by_city.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 08_salary_by_city.png")

# ── CHART 9: Vacancies by Sector (bar) ───────────────────────────────────────
print("[Chart 9] Vacancies by Sector (Graduate postings)...")
sector_counts = jobs.groupby("sector").size().reset_index(name="postings").sort_values("postings",ascending=True)
fig, ax = plt.subplots(figsize=(11,6))
ax.barh(sector_counts["sector"], sector_counts["postings"], color=NAVY, height=0.6)
for i,(sec,cnt) in enumerate(zip(sector_counts["sector"],sector_counts["postings"])):
    ax.text(cnt+2, i, str(cnt), va="center", fontsize=10)
ax.set_title("Graduate Analyst Job Postings by Sector (2024–2026 Sample)", fontsize=13, fontweight="bold", color=NAVY, pad=15)
ax.set_xlabel("Number of Postings")
ax.text(0.01,-0.09,"Source: Reed & LinkedIn sample (n=600)  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/09_postings_by_sector.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 09_postings_by_sector.png")

# ── CHART 10: Experience Required in 'Graduate' Roles ─────────────────────────
print("[Chart 10] Experience Paradox...")
exp_counts = jobs["experience_required"].value_counts()
fig, ax = plt.subplots(figsize=(9,6))
colors_exp = [RED if "year" in str(e).lower() else GREEN for e in exp_counts.index]
bars = ax.bar(exp_counts.index, exp_counts.values, color=colors_exp, width=0.6)
for bar,val in zip(bars,exp_counts.values):
    pct = val/len(jobs)*100
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3, f"{pct:.1f}%", ha="center", fontsize=10, fontweight="bold", color=NAVY)
ax.set_title("Experience Required in 'Graduate/Entry-Level' Job Postings\n(The Experience Paradox)", fontsize=13, fontweight="bold", color=NAVY, pad=15)
ax.set_xlabel("Experience Required"); ax.set_ylabel("Number of Postings")
exp_pct = (jobs["requires_experience"].sum() / len(jobs) * 100)
ax.text(0.5,0.92,f"{exp_pct:.1f}% of 'entry-level' roles require prior experience",transform=ax.transAxes,ha="center",fontsize=11,color=RED,fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3",facecolor="#FEF2F2",edgecolor=RED))
ax.text(0.01,-0.1,"Source: Reed & LinkedIn sample (n=600)  |  Gaurav Indora, 2026",transform=ax.transAxes,fontsize=7.5,color="gray")
plt.tight_layout(); plt.savefig(f"{EXPORTS}/10_experience_paradox.png",dpi=150,bbox_inches="tight"); plt.close()
print("  ✓ Saved: 10_experience_paradox.png")

# ── STATISTICAL SUMMARY ────────────────────────────────────────────────────────
print("\n" + "="*65)
print("DESCRIPTIVE STATISTICS SUMMARY")
print("="*65)
print("\nEmployment Rate:")
print(emp["employment_rate_pct"].describe().round(2).to_string())
print("\nVacancies (thousands):")
print(vac["total_vacancies_thousands"].describe().round(1).to_string())
print(f"\nGraduate salary (midpoint) — where disclosed:")
print(jobs["salary_midpoint"].dropna().describe().round(0).to_string())
print(f"\nExperience Paradox: {exp_pct:.1f}% of 'entry-level' roles require prior experience")
print(f"London's share of postings: {jobs['is_london'].mean()*100:.1f}%")
print(f"Visa sponsorship offered: {(jobs['visa_sponsorship']=='Yes').mean()*100:.1f}% of postings")
print(f"\nTop 5 in-demand skills:")
print(skills.head(5)[["rank","skill","pct_of_postings"]].to_string(index=False))

print("\n✓ All EDA charts saved to dashboards/exports/")
