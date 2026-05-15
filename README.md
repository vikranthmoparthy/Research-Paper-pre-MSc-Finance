# Repository Map

.
├── Main_Pipeline/
│   ├── extract_acquiror_target_ticker.py   # Extracts unique tickers from Zephyr for WRDS queries
│   ├── wrds_ticker_for_CAR_extraction.py   # Formats ticker strings for the WRDS Event Study tool
│   ├── merge_1.py                          # Initial alignment of CRSP and Zephyr data
│   ├── merge_2.py                          # Intermediate data cleaning and merging
│   └── final_merge.py                      # Master processing: Orbis quirks, Percent_Stock, and US filter
│
├── Regression/
│   ├── regression.py                       # OLS regression with HC3 robust standard errors
│   ├── update_descriptive_statistics.py    # Sub-group analysis split by median Relative Size
│   ├── Master_Regression_Dataset.csv       # Final merged input for statistical analysis
│   └── Target_Size_Descriptives.csv        # Summary table output (All, Small, and Large)
│
└── Visualisation/
    ├── wrds_car_extraction.py              # Preps Ticker/Date pairs for AAR robustness data
    ├── abret55graph.py                     # Plots Average Abnormal Returns (AAR) for window [-5, +5]
    ├── abret55.csv                         # Daily abnormal return data from WRDS
    └── CAR55_Event_Study_Plot.png          # High-resolution AAR visualization

---

# Script Descriptions

## Main Pipeline

extract_acquiror_target_ticker.py  
Extracts all unique acquiror and target tickers from the Zephyr export to ensure the CRSP/WRDS data pull covers all firms in the final sample.

wrds_ticker_for_CAR_extraction.py  
Formats ticker strings into the vertical string format required by WRDS for Cumulative Abnormal Return (CAR) extraction.

merge_1.py  
Initial alignment of CRSP market data with Zephyr deal-level data.

merge_2.py  
Intermediate cleaning and merging step that refines dataset structure and resolves mismatches.

final_merge.py  
Primary data pipeline engine:
- Fixes Orbis multi-row duplication issue via forward-filling  
- Constructs Percent_Stock (equity share of payment)  
- Filters US-to-US transactions  
- Builds Public_Target dummy using ticker/date matching  

---

## Regression

regression.py  
Runs OLS regressions using HC3 robust standard errors to correct for heteroskedasticity and high kurtosis (~40) in residuals.

update_descriptive_statistics.py  
Produces summary statistics split by median Relative_Size:
- All deals  
- Small targets  
- Large targets  

Includes:
- t-tests  
- non-parametric sign tests  
- rank tests for robustness under non-normal returns  

Master_Regression_Dataset.csv  
Final cleaned dataset used for regression analysis.

Target_Size_Descriptives.csv  
Output table summarizing subgroup statistics.

---

## Visualisation

wrds_car_extraction.py  
Extracts ticker–event date pairs into WRDS-compatible format for abnormal return robustness checks.

abret55graph.py  
Generates Average Abnormal Return (AAR) plot for event window [-5, +5], highlighting event day (t = 0).

abret55.csv  
Daily abnormal return data used for plotting and robustness analysis.

CAR55_Event_Study_Plot.png  
Final high-resolution event study visualization.