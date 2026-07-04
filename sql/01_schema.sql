-- ============================================================
-- UK Job Market Analysis — Database Schema
-- Author: Gaurav Indora
-- Database: SQLite / PostgreSQL compatible
-- Purpose: Relational database for all UK labour market data
-- Skills: SQL, Data Modelling, Business Intelligence
-- ============================================================

-- ── 1. EMPLOYMENT ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS employment (
    id                        INTEGER PRIMARY KEY AUTOINCREMENT,
    period                    TEXT NOT NULL UNIQUE,      -- e.g. '2020Q1'
    year                      INTEGER NOT NULL,
    quarter                   TEXT NOT NULL,             -- 'Q1' to 'Q4'
    employment_rate_pct       REAL,
    unemployment_rate_pct     REAL,
    inactivity_rate_pct       REAL,
    employed_thousands        REAL,
    unemployed_thousands      REAL,
    economically_inactive_thousands REAL,
    full_time_thousands       REAL,
    part_time_thousands       REAL,
    self_employed_thousands   REAL,
    employment_gap_vs_2019    REAL,   -- deviation from pre-pandemic baseline
    note                      TEXT
);

-- ── 2. VACANCIES ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS vacancies (
    id                            INTEGER PRIMARY KEY AUTOINCREMENT,
    period                        TEXT NOT NULL UNIQUE,
    year                          INTEGER NOT NULL,
    quarter                       TEXT NOT NULL,
    total_vacancies_thousands     REAL,
    finance_vacancies             REAL,
    technology_vacancies          REAL,
    healthcare_vacancies          REAL,
    retail_vacancies              REAL,
    manufacturing_vacancies       REAL,
    hospitality_vacancies         REAL,
    professional_services_vacancies REAL,
    public_admin_vacancies        REAL,
    vacancies_vs_peak_pct         REAL,   -- % of 2022 peak
    vacancies_vs_prepandemic_pct  REAL,
    qoq_change_thousands          REAL,
    qoq_change_pct                REAL,
    note                          TEXT
);

-- ── 3. ECONOMIC INDICATORS ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS economic_indicators (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    period                TEXT NOT NULL UNIQUE,         -- 'YYYY-MM'
    year                  INTEGER,
    month                 INTEGER,
    cpi_pct               REAL,
    boe_target_pct        REAL DEFAULT 2.0,
    base_rate_pct         REAL,
    real_rate             REAL,                         -- base rate - CPI
    inflation_target_miss REAL,                         -- CPI - 2.0
    rolling_3m_avg_cpi    REAL,
    above_target          TEXT,
    note                  TEXT
);

-- ── 4. GDP ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gdp (
    id                        INTEGER PRIMARY KEY AUTOINCREMENT,
    period                    TEXT NOT NULL UNIQUE,
    year                      INTEGER,
    quarter                   TEXT,
    gdp_growth_pct            REAL,
    gdp_gbp_billions          REAL,
    cumulative_growth_vs_2019Q4 REAL,
    rolling_annual_growth     REAL,
    recession_indicator       INTEGER DEFAULT 0,        -- 1 = two consecutive -ve qtrs
    above_pre_covid           TEXT,
    note                      TEXT
);

-- ── 5. EARNINGS ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS earnings (
    id                                INTEGER PRIMARY KEY AUTOINCREMENT,
    period                            TEXT NOT NULL UNIQUE,
    year                              INTEGER,
    quarter                           TEXT,
    avg_weekly_earnings_nominal_gbp   REAL,
    avg_weekly_earnings_real_gbp      REAL,
    annual_salary_nominal_gbp         REAL,
    annual_salary_real_gbp            REAL,
    note                              TEXT
);

-- ── 6. JOB POSTINGS ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS job_postings (
    posting_id            INTEGER PRIMARY KEY,
    job_title             TEXT,
    company               TEXT,
    sector                TEXT,
    city                  TEXT,
    salary_min_gbp        REAL,
    salary_max_gbp        REAL,
    salary_midpoint       REAL,
    has_salary            INTEGER DEFAULT 0,            -- 1 = salary disclosed
    experience_required   TEXT,
    requires_experience   INTEGER DEFAULT 0,            -- 1 = requires prior exp
    degree_required       TEXT,
    skills_required       TEXT,
    skill_count           INTEGER,
    working_arrangement   TEXT,
    visa_sponsorship      TEXT,
    date_posted           TEXT,
    applicant_count       INTEGER,
    level                 TEXT,
    is_london             INTEGER DEFAULT 0
);

-- ── INDEXES ────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_emp_year       ON employment(year);
CREATE INDEX IF NOT EXISTS idx_vac_year       ON vacancies(year);
CREATE INDEX IF NOT EXISTS idx_eco_year_month ON economic_indicators(year, month);
CREATE INDEX IF NOT EXISTS idx_gdp_year       ON gdp(year);
CREATE INDEX IF NOT EXISTS idx_jobs_sector    ON job_postings(sector);
CREATE INDEX IF NOT EXISTS idx_jobs_city      ON job_postings(city);
CREATE INDEX IF NOT EXISTS idx_jobs_salary    ON job_postings(salary_midpoint);

SELECT 'Schema created successfully. Tables: employment, vacancies, economic_indicators, gdp, earnings, job_postings' AS status;
