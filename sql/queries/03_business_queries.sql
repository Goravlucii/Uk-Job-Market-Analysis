-- ============================================================
-- UK Job Market Analysis — Business Query Library
-- Author: Gaurav Indora
-- 25 queries answering real business questions
-- Skills: SQL, JOINs, CTEs, Window Functions, Aggregates
-- ============================================================

-- ══════════════════════════════════════════════════════════════
-- SECTION A: LABOUR MARKET RECOVERY
-- ══════════════════════════════════════════════════════════════

-- Q1: Employment rate: current vs pre-pandemic baseline
-- Answers RQ-01
SELECT
    period,
    employment_rate_pct,
    76.6 AS prepandemic_baseline_pct,
    ROUND(employment_rate_pct - 76.6, 2) AS gap_vs_baseline,
    CASE WHEN employment_rate_pct >= 76.6 THEN 'AT/ABOVE BASELINE' ELSE 'BELOW BASELINE' END AS recovery_status
FROM employment
WHERE year >= 2019
ORDER BY period;

-- Q2: Peak unemployment during COVID vs 2008 crisis
-- Answers RQ-04
SELECT
    'COVID-19 (2020)'          AS crisis_period,
    MAX(unemployment_rate_pct) AS peak_unemployment_pct,
    MIN(period)                AS from_period
FROM employment WHERE year BETWEEN 2020 AND 2021
UNION ALL
SELECT '2008 Financial Crisis', 8.1, '2009Q4'  -- ONS recorded peak
UNION ALL
SELECT 'Pre-pandemic 2019',
    MIN(unemployment_rate_pct), MIN(period) FROM employment WHERE year=2019;

-- Q3: Sector vacancies — which recovered fastest?
-- Answers RQ-05
WITH prepandemic AS (
    SELECT
        ROUND(AVG(finance_vacancies),1)              AS fin_base,
        ROUND(AVG(technology_vacancies),1)           AS tech_base,
        ROUND(AVG(healthcare_vacancies),1)           AS health_base,
        ROUND(AVG(hospitality_vacancies),1)          AS hosp_base,
        ROUND(AVG(professional_services_vacancies),1) AS prof_base
    FROM vacancies WHERE year = 2019
)
SELECT
    v.period,
    ROUND(v.finance_vacancies / p.fin_base * 100, 1)               AS finance_recovery_pct,
    ROUND(v.technology_vacancies / p.tech_base * 100, 1)           AS tech_recovery_pct,
    ROUND(v.healthcare_vacancies / p.health_base * 100, 1)         AS health_recovery_pct,
    ROUND(v.hospitality_vacancies / p.hosp_base * 100, 1)         AS hospitality_recovery_pct,
    ROUND(v.professional_services_vacancies / p.prof_base * 100, 1) AS professional_recovery_pct
FROM vacancies v, prepandemic p
WHERE v.year >= 2020 ORDER BY v.period;

-- Q4: Full-time vs part-time employment split
-- Answers RQ-06
SELECT
    period,
    full_time_thousands,
    part_time_thousands,
    self_employed_thousands,
    ROUND(full_time_thousands * 100.0 / employed_thousands, 1) AS fulltime_share_pct,
    ROUND(part_time_thousands * 100.0 / employed_thousands, 1) AS parttime_share_pct
FROM employment
WHERE year >= 2019
ORDER BY period;

-- Q5: Year-over-year employment change using LAG (window function)
SELECT
    period,
    employment_rate_pct,
    LAG(employment_rate_pct, 4) OVER (ORDER BY period) AS same_qtr_last_year,
    ROUND(employment_rate_pct - LAG(employment_rate_pct, 4) OVER (ORDER BY period), 2) AS yoy_change_pp
FROM employment
WHERE year >= 2019
ORDER BY period;

-- ══════════════════════════════════════════════════════════════
-- SECTION B: ECONOMIC CONDITIONS
-- ══════════════════════════════════════════════════════════════

-- Q6: Months CPI was above BoE 2% target by year
-- Answers RQ-09
SELECT
    year,
    COUNT(*) AS total_months,
    SUM(CASE WHEN cpi_pct > 2.0 THEN 1 ELSE 0 END) AS months_above_target,
    ROUND(MAX(cpi_pct), 1) AS peak_cpi,
    ROUND(AVG(cpi_pct), 2) AS avg_cpi
FROM economic_indicators
GROUP BY year
ORDER BY year;

-- Q7: Base rate change history with cumulative change
-- Answers RQ-10
SELECT
    period,
    base_rate_pct,
    LAG(base_rate_pct) OVER (ORDER BY period) AS prev_month_rate,
    ROUND(base_rate_pct - LAG(base_rate_pct) OVER (ORDER BY period), 2) AS monthly_change,
    ROUND(base_rate_pct - 0.1, 2) AS change_from_covid_low
FROM economic_indicators
WHERE base_rate_pct != LAG(base_rate_pct) OVER (ORDER BY period)
   OR period = '2020-01'
ORDER BY period;

-- Q8: Identify technical recession periods (2 consecutive negative GDP quarters)
-- Answers RQ-11
WITH gdp_flags AS (
    SELECT
        period,
        gdp_growth_pct,
        LAG(gdp_growth_pct) OVER (ORDER BY period) AS prev_quarter,
        LEAD(gdp_growth_pct) OVER (ORDER BY period) AS next_quarter
    FROM gdp
)
SELECT
    period,
    gdp_growth_pct,
    prev_quarter,
    CASE
        WHEN gdp_growth_pct < 0 AND prev_quarter < 0 THEN 'RECESSION CONFIRMED'
        WHEN gdp_growth_pct < 0 THEN 'Negative (monitoring)'
        ELSE 'Positive'
    END AS recession_status
FROM gdp_flags
WHERE year >= 2020
ORDER BY period;

-- Q9: Correlation proxy — base rate vs vacancies (quarterly join)
-- Answers H2
SELECT
    e.period,
    e.avg_base_rate_pct AS base_rate,
    v.total_vacancies_thousands AS vacancies,
    e.avg_cpi_pct AS cpi,
    g.gdp_growth_pct AS gdp_growth
FROM (
    SELECT
        period,
        ROUND(AVG(base_rate_pct),2) AS avg_base_rate_pct,
        ROUND(AVG(cpi_pct),2) AS avg_cpi_pct
    FROM economic_indicators
    GROUP BY SUBSTR(period,1,4) || 'Q' ||
             CASE WHEN CAST(SUBSTR(period,6,2) AS INTEGER) <= 3 THEN '1'
                  WHEN CAST(SUBSTR(period,6,2) AS INTEGER) <= 6 THEN '2'
                  WHEN CAST(SUBSTR(period,6,2) AS INTEGER) <= 9 THEN '3' ELSE '4' END
) e
JOIN vacancies v ON e.period = v.period
JOIN gdp g ON e.period = g.period
ORDER BY e.period;

-- Q10: Real wage vs CPI — which years saw real pay cuts?
-- Answers H3
SELECT
    ea.period,
    ea.avg_weekly_earnings_nominal_gbp   AS nominal_weekly_gbp,
    ea.avg_weekly_earnings_real_gbp      AS real_weekly_gbp,
    ROUND(ea.avg_weekly_earnings_real_gbp - LAG(ea.avg_weekly_earnings_real_gbp,4) OVER (ORDER BY ea.period),2) AS real_yoy_change_gbp,
    ROUND((ea.avg_weekly_earnings_real_gbp / LAG(ea.avg_weekly_earnings_real_gbp,4) OVER (ORDER BY ea.period) - 1)*100, 2) AS real_yoy_change_pct,
    CASE WHEN ea.avg_weekly_earnings_real_gbp < LAG(ea.avg_weekly_earnings_real_gbp,4) OVER (ORDER BY ea.period) THEN 'REAL PAY CUT' ELSE 'Real pay growth' END AS verdict
FROM earnings ea
ORDER BY ea.period;

-- ══════════════════════════════════════════════════════════════
-- SECTION C: GRADUATE VACANCY ANALYSIS
-- ══════════════════════════════════════════════════════════════

-- Q11: Graduate postings by city with average salary
-- Answers RQ-20, RQ-21
SELECT
    city,
    COUNT(*) AS total_postings,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM job_postings),1) AS share_pct,
    ROUND(AVG(CASE WHEN salary_midpoint IS NOT NULL THEN salary_midpoint END),0) AS avg_salary_gbp,
    ROUND(AVG(applicant_count),0) AS avg_applicants_per_posting,
    SUM(CASE WHEN requires_experience=1 THEN 1 ELSE 0 END) AS with_exp_req
FROM job_postings
GROUP BY city
ORDER BY total_postings DESC;

-- Q12: Experience paradox — 'entry level' roles requiring experience
-- Answers RQ-22, H5
SELECT
    experience_required,
    COUNT(*) AS postings,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM job_postings),1) AS share_pct,
    ROUND(AVG(salary_midpoint),0) AS avg_salary_gbp,
    ROUND(AVG(applicant_count),0) AS avg_applicants
FROM job_postings
GROUP BY experience_required
ORDER BY postings DESC;

-- Q13: Salary distribution by sector with quartiles
-- Answers RQ-21
SELECT
    sector,
    COUNT(*) AS postings,
    SUM(has_salary) AS with_salary,
    ROUND(MIN(salary_midpoint),0) AS min_salary,
    ROUND(AVG(salary_midpoint),0) AS avg_salary,
    ROUND(MAX(salary_midpoint),0) AS max_salary
FROM job_postings
WHERE salary_midpoint IS NOT NULL
GROUP BY sector
ORDER BY avg_salary DESC;

-- Q14: Visa sponsorship availability
-- Answers RQ-26
SELECT
    visa_sponsorship,
    COUNT(*) AS postings,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM job_postings),1) AS pct_of_all_postings,
    ROUND(AVG(salary_midpoint),0) AS avg_salary_gbp
FROM job_postings
GROUP BY visa_sponsorship;

-- Q15: Working arrangement breakdown
-- Answers RQ-23
SELECT
    working_arrangement,
    COUNT(*) AS postings,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM job_postings),1) AS share_pct,
    ROUND(AVG(salary_midpoint),0) AS avg_salary_gbp
FROM job_postings
GROUP BY working_arrangement
ORDER BY postings DESC;

-- ══════════════════════════════════════════════════════════════
-- SECTION D: SALARY & SKILLS ANALYSIS
-- ══════════════════════════════════════════════════════════════

-- Q16: Top job titles by posting volume and avg salary
SELECT
    job_title,
    COUNT(*) AS postings,
    ROUND(AVG(salary_midpoint),0) AS avg_salary_gbp,
    ROUND(AVG(applicant_count),0) AS avg_applicants,
    SUM(is_london) AS london_postings
FROM job_postings
GROUP BY job_title
ORDER BY postings DESC
LIMIT 15;

-- Q17: London premium — salary comparison
-- Answers H6, H9
SELECT
    CASE WHEN is_london=1 THEN 'London' ELSE 'Rest of UK' END AS location,
    COUNT(*) AS postings,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM job_postings),1) AS share_pct,
    ROUND(AVG(salary_midpoint),0) AS avg_salary_gbp,
    ROUND(AVG(applicant_count),0) AS avg_applicants_per_role,
    SUM(CASE WHEN requires_experience=1 THEN 1 ELSE 0 END) AS with_exp_requirement
FROM job_postings
GROUP BY is_london;

-- Q18: Salary tier analysis (banding)
SELECT
    CASE
        WHEN salary_midpoint < 25000 THEN '< £25k'
        WHEN salary_midpoint < 30000 THEN '£25k – £30k'
        WHEN salary_midpoint < 35000 THEN '£30k – £35k'
        WHEN salary_midpoint < 40000 THEN '£35k – £40k'
        ELSE '£40k+'
    END AS salary_band,
    COUNT(*) AS postings,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM job_postings WHERE salary_midpoint IS NOT NULL),1) AS pct
FROM job_postings
WHERE salary_midpoint IS NOT NULL
GROUP BY salary_band
ORDER BY MIN(salary_midpoint);

-- ══════════════════════════════════════════════════════════════
-- SECTION E: KPI DASHBOARD QUERIES
-- ══════════════════════════════════════════════════════════════

-- Q19: Executive KPI summary — current vs baseline
-- Powers KPI dashboard page
WITH latest_emp AS (SELECT * FROM employment ORDER BY period DESC LIMIT 1),
     baseline   AS (SELECT * FROM employment WHERE period='2019Q4'),
     latest_vac AS (SELECT * FROM vacancies ORDER BY period DESC LIMIT 1),
     latest_eco AS (SELECT * FROM economic_indicators ORDER BY period DESC LIMIT 1)
SELECT
    le.employment_rate_pct                   AS current_employment_rate,
    b.employment_rate_pct                    AS baseline_employment_rate,
    le.employment_rate_pct - b.employment_rate_pct AS employment_gap,
    le.unemployment_rate_pct                 AS current_unemployment_rate,
    lv.total_vacancies_thousands             AS current_vacancies_k,
    eco.cpi_pct                             AS current_cpi_pct,
    eco.base_rate_pct                       AS current_base_rate_pct
FROM latest_emp le, baseline b, latest_vac lv, latest_eco eco;

-- Q20: Quarterly trend for dashboard time series
SELECT
    e.period,
    e.employment_rate_pct,
    e.unemployment_rate_pct,
    v.total_vacancies_thousands,
    g.gdp_growth_pct
FROM employment e
JOIN vacancies v ON e.period = v.period
JOIN gdp g ON e.period = g.period
ORDER BY e.period;

-- ══════════════════════════════════════════════════════════════
-- SECTION F: ADVANCED — CTEs + WINDOW FUNCTIONS
-- ══════════════════════════════════════════════════════════════

-- Q21: Ranking quarters by employment performance using RANK()
SELECT
    period,
    employment_rate_pct,
    RANK() OVER (ORDER BY employment_rate_pct DESC)  AS rank_best_employment,
    RANK() OVER (ORDER BY unemployment_rate_pct ASC) AS rank_lowest_unemployment,
    NTILE(4) OVER (ORDER BY employment_rate_pct DESC) AS quartile
FROM employment
WHERE year >= 2020
ORDER BY rank_best_employment;

-- Q22: 4-quarter rolling average vacancies (smoothed trend)
SELECT
    period,
    total_vacancies_thousands AS actual,
    ROUND(AVG(total_vacancies_thousands) OVER (ORDER BY period ROWS BETWEEN 3 PRECEDING AND CURRENT ROW), 1) AS rolling_4q_avg,
    ROUND(total_vacancies_thousands - AVG(total_vacancies_thousands) OVER (ORDER BY period ROWS BETWEEN 3 PRECEDING AND CURRENT ROW), 1) AS deviation_from_trend
FROM vacancies
ORDER BY period;

-- Q23: CTE — Identify economic stress periods (high CPI + high rates)
WITH monthly_stress AS (
    SELECT
        period, year, month,
        cpi_pct, base_rate_pct,
        CASE WHEN cpi_pct > 5 AND base_rate_pct > 1 THEN 1 ELSE 0 END AS stress_indicator,
        CASE
            WHEN cpi_pct > 10 THEN 'SEVERE'
            WHEN cpi_pct > 5  THEN 'HIGH'
            WHEN cpi_pct > 2  THEN 'MODERATE'
            ELSE 'LOW'
        END AS inflation_severity
    FROM economic_indicators
),
stress_summary AS (
    SELECT
        year,
        SUM(stress_indicator) AS stress_months,
        ROUND(AVG(cpi_pct),2) AS avg_cpi,
        ROUND(AVG(base_rate_pct),2) AS avg_rate
    FROM monthly_stress
    GROUP BY year
)
SELECT
    ms.period, ms.cpi_pct, ms.base_rate_pct,
    ms.inflation_severity,
    ss.stress_months AS stress_months_in_year
FROM monthly_stress ms
JOIN stress_summary ss ON ms.year = ss.year
ORDER BY ms.period;

-- Q24: Data validation query — row counts and coverage
SELECT 'employment'           AS table_name, COUNT(*) AS rows, MIN(period) AS from_period, MAX(period) AS to_period FROM employment
UNION ALL
SELECT 'vacancies',            COUNT(*), MIN(period), MAX(period) FROM vacancies
UNION ALL
SELECT 'economic_indicators',  COUNT(*), MIN(period), MAX(period) FROM economic_indicators
UNION ALL
SELECT 'gdp',                  COUNT(*), MIN(period), MAX(period) FROM gdp
UNION ALL
SELECT 'earnings',             COUNT(*), MIN(period), MAX(period) FROM earnings
UNION ALL
SELECT 'job_postings',         COUNT(*), MIN(date_posted), MAX(date_posted) FROM job_postings;

-- Q25: Graduate market health score (composite KPI)
-- Combines: employment rate, vacancy level, real wages, CPI proximity to target
WITH latest AS (
    SELECT
        e.employment_rate_pct,
        v.total_vacancies_thousands,
        eco.cpi_pct,
        eco.base_rate_pct
    FROM employment e
    JOIN vacancies v ON e.period = v.period
    JOIN (SELECT * FROM economic_indicators ORDER BY period DESC LIMIT 1) eco ON 1=1
    ORDER BY e.period DESC LIMIT 1
)
SELECT
    employment_rate_pct,
    ROUND((employment_rate_pct / 76.6) * 25, 1)        AS employment_score_25,
    ROUND((total_vacancies_thousands / 1295) * 25, 1)  AS vacancy_score_25,
    ROUND((1 - ABS(cpi_pct - 2.0) / 9.1) * 25, 1)    AS inflation_score_25,
    ROUND((1 - base_rate_pct / 5.25) * 25, 1)         AS rate_score_25,
    ROUND(
        (employment_rate_pct / 76.6) * 25 +
        (total_vacancies_thousands / 1295) * 25 +
        (1 - ABS(cpi_pct - 2.0) / 9.1) * 25 +
        (1 - base_rate_pct / 5.25) * 25, 1
    ) AS composite_market_health_score_100
FROM latest;
