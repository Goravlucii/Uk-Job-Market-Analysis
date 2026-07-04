# ============================================================
# UK Job Market Analysis — R Forecasting Models
# Author: Gaurav Indora
# Purpose: Time series forecasting 2027-2030 using ARIMA + regression
# Skills: R Programming, Forecasting, Statistical Analysis
# ============================================================
# Required packages: forecast, tseries, ggplot2, dplyr, readr
# Install: install.packages(c("forecast","tseries","ggplot2","dplyr","readr"))
# ============================================================

library(forecast)
library(tseries)
library(ggplot2)
library(dplyr)
library(readr)

cat("========================================================\n")
cat("UK JOB MARKET ANALYSIS — FORECASTING MODELS\n")
cat(paste0("Run at: ", Sys.time(), "\n"))
cat("========================================================\n\n")

# ── Set Paths ─────────────────────────────────────────────────
ROOT         <- dirname(rstudioapi::getActiveDocumentContext()$path)
if (!nchar(ROOT)) ROOT <- getwd()
CLEAN        <- file.path(ROOT, "..", "data", "cleaned")
OUTPUTS      <- file.path(ROOT, "forecast_outputs")
dir.create(OUTPUTS, showWarnings=FALSE)

# ── Load Data ─────────────────────────────────────────────────
master <- read_csv(file.path(CLEAN, "master_labour_market.csv"), show_col_types=FALSE)
emp    <- read_csv(file.path(CLEAN, "employment_clean.csv"),      show_col_types=FALSE)
vac    <- read_csv(file.path(CLEAN, "vacancies_clean.csv"),       show_col_types=FALSE)

cat("[1] Data loaded:\n")
cat(paste0("    Master: ", nrow(master), " quarters\n"))
cat(paste0("    Employment: ", nrow(emp), " quarters\n"))
cat(paste0("    Vacancies: ", nrow(vac), " quarters\n\n"))

# ── Helper: MAPE ──────────────────────────────────────────────
mape <- function(actual, predicted) {
  mean(abs((actual - predicted) / actual), na.rm=TRUE) * 100
}

# ════════════════════════════════════════════════════════════════
# MODEL 1: ARIMA — Vacancy Volume Forecast 2027-2030
# ════════════════════════════════════════════════════════════════
cat("[Model 1] ARIMA — UK Vacancy Volume\n")
vac_ts <- ts(vac$total_vacancies_thousands, start=c(2019,1), frequency=4)

# Stationarity test (ADF)
adf_result <- adf.test(vac_ts)
cat(paste0("    ADF test p-value: ", round(adf_result$p.value, 4),
           ifelse(adf_result$p.value < 0.05, " (stationary)", " (non-stationary — differencing needed)"), "\n"))

# Auto ARIMA (Box-Jenkins automatic selection)
arima_vac <- auto.arima(vac_ts,
                         d=NA, D=NA,
                         stepwise=FALSE,
                         approximation=FALSE,
                         trace=FALSE)
cat(paste0("    Best model: ARIMA", paste0(arima_vac$arma[c(1,6,2,3,7,4,5)], collapse=",")))
cat(paste0("\n    AIC: ", round(AIC(arima_vac), 2), "\n"))

# Backtest: fit on 2019-2022, test on 2023-2024
train_end <- c(2022, 4)
train_ts  <- window(vac_ts, end=train_end)
arima_train <- auto.arima(train_ts, stepwise=FALSE, trace=FALSE)
test_ts   <- window(vac_ts, start=c(2023,1))
fcast_backtest <- forecast(arima_train, h=length(test_ts))
mape_val <- mape(as.numeric(test_ts), as.numeric(fcast_backtest$mean))
cat(paste0("    Backtest MAPE: ", round(mape_val, 2), "%\n"))

# Full forecast 2026 Q2 → 2030 Q4 (18 quarters)
fcast_vac <- forecast(arima_vac, h=18, level=c(80, 95))
fcast_df  <- data.frame(
  period  = paste0(rep(2026:2030, each=4)[1:18], "Q", rep(1:4, 5)[1:18]),
  year    = rep(2026:2030, each=4)[1:18],
  quarter = paste0("Q", rep(1:4, 5)[1:18]),
  forecast= as.numeric(fcast_vac$mean),
  lo80    = as.numeric(fcast_vac$lower[,1]),
  hi80    = as.numeric(fcast_vac$upper[,1]),
  lo95    = as.numeric(fcast_vac$lower[,2]),
  hi95    = as.numeric(fcast_vac$upper[,2]),
  model   = "ARIMA",
  series  = "Vacancies (000s)"
)
write_csv(fcast_df, file.path(OUTPUTS, "vacancy_forecast_2030.csv"))
cat(paste0("    2028 forecast: ", round(mean(fcast_df$forecast[fcast_df$year==2028]),0), "k vacancies\n"))
cat(paste0("    2030 forecast: ", round(mean(fcast_df$forecast[fcast_df$year==2030]),0), "k vacancies\n"))
cat("    ✓ Saved: vacancy_forecast_2030.csv\n\n")

# ════════════════════════════════════════════════════════════════
# MODEL 2: ARIMA — Employment Rate Forecast
# ════════════════════════════════════════════════════════════════
cat("[Model 2] ARIMA — UK Employment Rate\n")
emp_ts <- ts(emp$employment_rate_pct, start=c(2019,1), frequency=4)
arima_emp <- auto.arima(emp_ts, stepwise=FALSE, trace=FALSE)
cat(paste0("    Best model: ARIMA(", paste(arima_emp$arma[c(1,6,2,3,7,4,5)],collapse=","), ")\n"))

fcast_emp <- forecast(arima_emp, h=20, level=c(80,95))
emp_fcast_df <- data.frame(
  period  = paste0(rep(2026:2031,each=4)[1:20],"Q",rep(1:4,6)[1:20]),
  year    = rep(2026:2031,each=4)[1:20],
  quarter = paste0("Q",rep(1:4,6)[1:20]),
  forecast= pmin(as.numeric(fcast_emp$mean), 78),  # cap at realistic max
  lo80    = as.numeric(fcast_emp$lower[,1]),
  hi80    = as.numeric(fcast_emp$upper[,1]),
  lo95    = as.numeric(fcast_emp$lower[,2]),
  hi95    = as.numeric(fcast_emp$upper[,2]),
  model   = "ARIMA",
  series  = "Employment Rate (%)"
)
write_csv(emp_fcast_df, file.path(OUTPUTS, "employment_forecast_2030.csv"))

baseline_return <- emp_fcast_df %>%
  filter(forecast >= 76.6) %>%
  slice(1)

if (nrow(baseline_return) > 0) {
  cat(paste0("    Projected return to 76.6% baseline: ", baseline_return$period[1], "\n"))
} else {
  cat("    H10 CONFIRMED: Employment rate does NOT reach 76.6% baseline by 2030\n")
}
cat("    ✓ Saved: employment_forecast_2030.csv\n\n")

# ════════════════════════════════════════════════════════════════
# MODEL 3: Linear Regression — Graduate Salary Forecast
# ════════════════════════════════════════════════════════════════
cat("[Model 3] Linear Regression — Graduate Salary Trajectory\n")
salaries <- data.frame(
  year    = 2019:2026,
  salary  = c(24100, 23200, 23600, 24800, 26100, 27200, 29200, 31000)
)
sal_model <- lm(salary ~ year, data=salaries)
r2 <- summary(sal_model)$r.squared
cat(paste0("    R² = ", round(r2,3), "\n"))
cat(paste0("    Annual salary growth: +£", round(coef(sal_model)["year"],0), "/year\n"))

future_years <- data.frame(year=2027:2030)
sal_forecast <- predict(sal_model, future_years, interval="prediction", level=0.95)
sal_fcast_df <- cbind(future_years, as.data.frame(sal_forecast))
names(sal_fcast_df) <- c("year","forecast_gbp","lo95_gbp","hi95_gbp")
write_csv(sal_fcast_df, file.path(OUTPUTS, "salary_forecast_2030.csv"))
cat("    Salary projections:\n")
for (i in 1:nrow(sal_fcast_df)) {
  cat(paste0("    ", sal_fcast_df$year[i], ": £",
             format(round(sal_fcast_df$forecast_gbp[i],0), big.mark=","),
             "  (95% CI: £", format(round(sal_fcast_df$lo95_gbp[i],0),big.mark=","),
             " – £", format(round(sal_fcast_df$hi95_gbp[i],0),big.mark=","), ")\n"))
}
cat("    ✓ Saved: salary_forecast_2030.csv\n\n")

# ════════════════════════════════════════════════════════════════
# MODEL 4: Regression — GDP Growth → Vacancies
# ════════════════════════════════════════════════════════════════
cat("[Model 4] Regression — GDP Growth vs Vacancies\n")
merged_gdp <- master %>%
  select(period, gdp_growth_pct, total_vacancies_thousands) %>%
  filter(!is.na(gdp_growth_pct) & !is.na(total_vacancies_thousands))

gdp_model <- lm(total_vacancies_thousands ~ gdp_growth_pct, data=merged_gdp)
r2_gdp    <- summary(gdp_model)$r.squared
p_val     <- summary(gdp_model)$coefficients["gdp_growth_pct", "Pr(>|t|)"]
slope     <- coef(gdp_model)["gdp_growth_pct"]

cat(paste0("    R² = ", round(r2_gdp,3), ",  p = ", round(p_val,4), "\n"))
cat(paste0("    1pp GDP growth → ", round(slope,0), "k additional vacancies\n"))
cat(paste0("    Significance: ", ifelse(p_val<0.05,"Statistically significant (p<0.05)","Not significant"), "\n\n"))

# ════════════════════════════════════════════════════════════════
# SCENARIO ANALYSIS
# ════════════════════════════════════════════════════════════════
cat("[Scenario Analysis] Three scenarios: Base / Optimistic / Pessimistic\n")
scenarios <- data.frame(
  year      = 2026:2030,
  base_vac  = c(893, 940, 985, 1020, 1055),
  opt_vac   = c(930, 1010, 1080, 1140, 1190),   # rate cuts accelerate hiring
  pess_vac  = c(870, 890, 905, 915, 920),        # AI displaces entry-level
  base_sal  = c(31000, 32800, 34600, 36400, 38200),
  opt_sal   = c(32000, 34500, 37200, 40100, 43200),
  pess_sal  = c(30000, 31200, 32500, 33800, 35100)
)
write_csv(scenarios, file.path(OUTPUTS, "scenario_analysis_2030.csv"))

cat("    Vacancy scenarios (2028 midpoint):\n")
cat(paste0("      Optimistic:  ", scenarios$opt_vac[scenarios$year==2028], "k\n"))
cat(paste0("      Base case:   ", scenarios$base_vac[scenarios$year==2028], "k\n"))
cat(paste0("      Pessimistic: ", scenarios$pess_vac[scenarios$year==2028], "k\n"))
cat("    ✓ Saved: scenario_analysis_2030.csv\n\n")

# ════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════
cat("========================================================\n")
cat("FORECASTING COMPLETE\n")
cat("Outputs in: r_models/forecast_outputs/\n")
cat("  ✓ vacancy_forecast_2030.csv\n")
cat("  ✓ employment_forecast_2030.csv\n")
cat("  ✓ salary_forecast_2030.csv\n")
cat("  ✓ scenario_analysis_2030.csv\n")
cat("========================================================\n")
