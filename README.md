# M&A Event Study Empirical Pipeline

---

## 1. Repository Map

```text
Research_Pipeline
├── Main_Pipeline
│   ├── .DS_Store
│   ├── Final_Event_Study_Merged.csv
│   ├── Master_Regression_Dataset.csv
│   ├── Master_Relative_Size_Data.csv
│   ├── UPDATE_2_Export 08_05_2026 09_45.csv
│   ├── WRDS_Acquiror_Tickers.txt
│   ├── WRDS_Robustness_Input.txt
│   ├── WRDS_Target_Tickers.txt
│   ├── extract_acquiror_target_ticker.py
│   ├── final_merge.py
│   ├── merge_1.py
│   ├── merge_2.py
│   ├── wrds_car_data.csv
│   └── wrds_ticker_for_CAR_extraction.py
│
├── Main_Regression
│   ├── Master_Regression_Dataset.csv
│   ├── Target_Size_Descriptives.csv
│   ├── regression.py
│   └── update_descriptive_statistics.py
│
├── Modified_Event_Window_Regression
│   ├── CAR205.csv
│   ├── CAR205_merge.py
│   ├── Master_Regression_Dataset.csv
│   ├── Master_Regression_Dataset_205.csv
│   ├── WRDS_Event_Study_Input_205.txt
│   ├── acquiror_ticker_extractor.py
│   └── regression2.py
│
├── Modified_Relative_Size_Regression
│   ├── Final_Event_Study_Merged_v2.csv
│   ├── Master_Regression_Dataset_v2.csv
│   ├── Master_Relative_Size_Data_v2.csv
│   ├── UPDATE_2_Export 08_05_2026 09_45.csv
│   ├── Wrds_car_data.csv
│   ├── final_merge_v2.py
│   ├── merge_1_v2.py
│   ├── merge_2_v2.py
│   └── regression3.py
│
└── Visualisation
    ├── AAR55_Event_Study_Plot.png
    ├── Master_Regression_Dataset.csv
    ├── WRDS_Robustness_Input.txt
    ├── abret55.csv
    ├── abret55graph.py
    └── wrds_car_extraction.py
```

---

## 2. Running Instructions

To run the analysis, execute the Python scripts in the following order within their respective folders:

### Main Pipeline
1. Run `extract_acquiror_target_ticker.py` to generate the ticker lists for WRDS.
2. Run `merge_1.py` to filter the deals and calculate the initial relative sizes.
3. Run `wrds_ticker_for_CAR_extraction.py` to create the input file needed to download your return data.
4. Download `wrds_car_data.csv` from WRDS and place it in the folder.
5. Run `merge_2.py` to merge the deal sizes with the WRDS return data.
6. Run `final_merge.py` to assemble the finalized dataset.

### Main Regression
1. Run `regression.py` to execute the primary statistical model.
2. Run `update_descriptive_statistics.py` to generate the summary statistics table.

### Modified Event Window Regression
1. Run `acquiror_ticker_extractor.py` to generate the list needed to download the longer-window returns.
2. Download `CAR205.csv` from WRDS and place it in the folder.
3. Run `CAR205_merge.py` to merge the extended-window returns into the dataset.
4. Run `regression2.py` to execute the robustness check.

### Modified Relative Size Regression
1. Run `merge_1_v2.py` to calculate relative sizes using stock prices from Day -50.
2. Run `merge_2_v2.py` to merge these new sizes with the CAR data.
3. Run `final_merge_v2.py` to build the robustness dataset.
4. Run `regression3.py` to execute the Day -50 regression model.

### Visualisation
1. Run `wrds_car_extraction.py` to create the WRDS input list for daily returns.
2. Download `abret55.csv` from WRDS and place it in the folder.
3. Run `abret55graph.py` to generate the visual plot of the stock returns.

---

## 3. File Descriptions

### Main Pipeline

| File | Description |
|---|---|
| `extract_acquiror_target_ticker.py` | Extracts unique acquirer and target ticker symbols from the Zephyr deal export. Removes empty entries, cleans whitespace, sorts alphabetically, and saves to text files for WRDS. |
| `merge_1.py` | Filters raw Zephyr data to isolate pure 100% takeovers and removes transactions within one year of each other. Merges with CRSP acquirer data to calculate relative sizes. |
| `merge_2.py` | Aligns relative size data with WRDS CAR using a forward chronological merge (four-day tolerance). Maps announcement dates to corresponding stock market performance windows. |
| `final_merge.py` | Fixes Zephyr's multi-row layout by combining payment rows and keeps only domestic US deals. Calculates stock payment percentage, identifies public targets, matches industry codes, and builds the final dataset. |
| `wrds_ticker_for_CAR_extraction.py` | Extracts unique acquirer tickers and announcement dates from the relative size data, formats dates to YYYYMMDD, and saves an input file for the WRDS Event Study tool. |
| `.DS_Store` | A macOS system file storing custom attributes of its containing folder. |
| `UPDATE_2_Export 08_05_2026 09_45.csv` | Raw export data from Zephyr containing the initial list of M&A deals. |
| `wrds_car_data.csv` | Spreadsheet from WRDS containing cumulative abnormal returns for involved companies. |
| `Master_Relative_Size_Data.csv` | Intermediate dataset storing calculated relative deal sizes before adding return data. |
| `Final_Event_Study_Merged.csv` | Combined dataset merging the relative size deal data with the WRDS stock return data. |
| `Master_Regression_Dataset.csv` | Finalized, clean dataset containing all variables needed to run the main statistical regressions. |
| `WRDS_Acquiror_Tickers.txt` | Clean list of acquirers' stock tickers to be uploaded to WRDS. |
| `WRDS_Target_Tickers.txt` | Clean list of targets' stock tickers to be uploaded to WRDS. |
| `WRDS_Robustness_Input.txt` | Text file linking acquirer tickers with specific event dates to pull targeted return data from WRDS. |

### Main Regression

| File | Description |
|---|---|
| `regression.py` | Runs the robust linear OLS regression for the main event window, applying HC3 robust standard errors to account for heteroskedasticity. |
| `update_descriptive_statistics.py` | Separates the master dataset into small and large subsamples based on median relative deal size. Calculates statistics and runs parametric/non-parametric significance tests. |
| `Master_Regression_Dataset.csv` | A copy of the finalized dataset used to run the main statistical model. |
| `Target_Size_Descriptives.csv` | A table summarizing statistical properties of the deals, split by large or small target company. |

### Modified Event Window Regression

| File | Description |
|---|---|
| `acquiror_ticker_extractor.py` | Extracts and cleans acquirer tickers and announcement dates from the final master dataset. Renames columns and formats dates to YYYYMMDD for WRDS. |
| `CAR205_merge.py` | Drops existing return variables from the master dataset and replaces them with CAR calculated over the [-20, +5] window using an inner join on ticker and date. |
| `regression2.py` | Executes regression using the [-20, +5] window dataset. Drops missing values, applies HC3 robust standard errors, and prints output. |
| `CAR205.csv` | Dataset of stock returns calculated over a 26-day window to check for early market rumors. |
| `Master_Regression_Dataset_205.csv` | Version of the final dataset replacing the standard return window with the extended 26-day window. |
| `WRDS_Event_Study_Input_205.txt` | Text file to query WRDS specifically for the extended 26-day event window returns. |

### Modified Relative Size Regression

| File | Description |
|---|---|
| `merge_1_v2.py` | Filters Zephyr data for 100% takeovers, removes deals within a one-year window, and matches with CRSP data shifted backward by 50 days to extract market capitalization. |
| `merge_2_v2.py` | Aligns Day -50 relative size data with CAR data using a forward chronological merge (four-day tolerance) to bridge calendar gaps cleanly. |
| `final_merge_v2.py` | Fixes Zephyr layout issues, filters for US deals, calculates stock percentages, matches industry codes, and applies a log transformation to the Day -50 market cap data. |
| `regression3.py` | Runs OLS regression using the Day -50 adjusted dataset. Cleans entries, applies HC3 errors, and prints the summary. |
| `UPDATE_2_Export 08_05_2026 09_45.csv` | Copy of the raw export data from Zephyr used to build the modified dataset. |
| `Wrds_car_data.csv` | Copy of the standard cumulative abnormal returns spreadsheet from WRDS. |
| `Master_Relative_Size_Data_v2.csv` | Modified intermediate dataset calculating deal sizes using stock prices from 50 days before announcement. |
| `Final_Event_Study_Merged_v2.csv` | Combined dataset linking the Day -50 modified size data with the stock returns. |
| `Master_Regression_Dataset_v2.csv` | Finalized dataset built to test if measuring company size 50 days early changes regression results. |

### Visualisation

| File | Description |
|---|---|
| `wrds_car_extraction.py` | Extracts unique acquirer tickers and announcement dates from the master regression dataset, reformats dates, removes duplicates, and generates a WRDS input file. |
| `abret55graph.py` | Processes CAR across a [-5, +5] window to calculate the Average Abnormal Return (AAR) for each day, then generates a line graph to visualize the data. |
| `AAR55_Event_Study_Plot.png` | An image of a line chart showing how the stock returns trended over the 11-day event window. |
| `Master_Regression_Dataset.csv` | A copy of the finalized dataset used to generate the ticker input file. |
| `WRDS_Robustness_Input.txt` | A text file used to pull the daily abnormal returns for the 11-day window from WRDS. |
| `abret55.csv` | A dataset containing the daily abnormal stock returns for the 11 days right around the deal announcement. |