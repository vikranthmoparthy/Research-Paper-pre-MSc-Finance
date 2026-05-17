# Research Pipeline

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
├── Modified Event Window Regression [-20, +5]
│   ├── CAR205.csv
│   ├── CAR205_merge.py
│   ├── Master_Regression_Dataset.csv
│   ├── Master_Regression_Dataset_205.csv
│   ├── WRDS_Event_Study_Input_205.txt
│   ├── acquiror_ticker_extractor.py
│   └── regression2.py
│
├── Modified Relative Size Regression (Market Cap -50)
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
Before running the analysis, download the following two files from GDrive and place a copy of each file in BOTH the "Main Pipeline" and "Modified Relative Size Regression (Market Cap -50)" folders:

csrp_acquiror_data.csv: https://drive.google.com/file/d/1cCAdUWZ-8Lk_cHhBiXby9r0ERvuPcIfe/view?usp=sharing
csrp_target_data.csv: https://drive.google.com/file/d/1MPW_31XlkszybJvNku7VT2T61nKUPJEu/view?usp=sharing

To run the analysis, execute the Python scripts in the following order within their respective folders:

### Main Pipeline
1. Run `merge_1.py` to filter the deals and calculate the initial relative sizes.
2. Run `merge_2.py` to merge the deal sizes with the WRDS return data.
3. Run `final_merge.py` to create the final dataset.

### Main Regression
1. Run `regression.py`, which give you the main event-window regression results.
2. Run `update_descriptive_statistics.py` to generate the descriptive statistics table.

### Modified Event Window Regression [-20, +5]
1. Run `CAR205_merge.py` to merge the [-20, +5] returns into the dataset.
2. Run `regression2.py` to run the updated regression

### Modified Relative Size Regression (Market Cap -50)
1. Run `merge_1_v2.py` to calculate relative sizes using stock prices from Day -50.
2. Run `merge_2_v2.py` to merge these new sizes with the CAR data.
3. Run `final_merge_v2.py` to build the final dataset.
4. Run `regression3.py` to execute the Day -50 regression model.

### Visualisation [-5, +5] AAR Graph
1. Run `abret55graph.py` to generate the plot of the [-5, +5] AAR returns.

---

## 3. File Descriptions

### Main Pipeline

| File | Description |
|---|---|
| `extract_acquiror_target_ticker.py` | Extracts unique acquirer and target ticker symbols from the Zephyr deal export. Removes empty entries, cleans whitespace, sorts alphabetically, and saves to text files for WRDS. |
| `merge_1.py` | Filters raw Zephyr data to isolate pure 100% takeovers and removes transactions within one year of each other. Merges with CRSP acquirer data to calculate relative sizes. |
| `merge_2.py` | Aligns relative size data with WRDS CAR using a forward chronological merge|
| `final_merge.py` | Combines payment rows and keeps only domestic US deals. Calculates stock payment percentage, identifies public targets, matches industry codes, and builds the final dataset. |
| `wrds_ticker_for_CAR_extraction.py` | Extracts unique acquirer tickers and announcement dates from the relative size data, formats dates to YYYYMMDD, and saves an input file for the WRDS Event Study tool. |
| `.DS_Store` | N/A |
| `UPDATE_2_Export 08_05_2026 09_45.csv` | Raw export data from Zephyr containing the initial list of M&A deals. |
| `wrds_car_data.csv` | Spreadsheet from WRDS containing CAR for involved acquiring firms. |
| `Master_Relative_Size_Data.csv` | Intermediate dataset storing calculated relative deal sizes before adding return data. |
| `Final_Event_Study_Merged.csv` | Combined dataset merging the relative size deal data with the WRDS stock return data. |
| `Master_Regression_Dataset.csv` | Final dataset containing all variables needed to run the main regression|
| `WRDS_Acquiror_Tickers.txt` | Clean list of acquirers' stock tickers, which were uploaded to WRDS.|
| `WRDS_Target_Tickers.txt` | Clean list of targets' stock tickers, which were uploaded to WRDS. |
| `WRDS_Robustness_Input.txt` | Text file linking acquirer tickers with event dates to request return data from WRDS. |

### Main Regression

| File | Description |
|---|---|
| `regression.py` | Runs the robust linear regression for the main event window|
| `update_descriptive_statistics.py` | Separates the master dataset into small and large samples based on median relative deal size. Then, calculates descriptive statistics for each group. |
| `Master_Regression_Dataset.csv` | A copy of the final dataset for the regression |
| `Target_Size_Descriptives.csv` | A table summarizing descriptive statistics of the deals, split by large or small target company.|

### Modified Event Window Regression [-20, +5]

| File | Description |
|---|---|
| `acquiror_ticker_extractor.py` | Extracts and cleans acquirer tickers and announcement dates from the final master dataset. Renames columns and formats dates to YYYYMMDD for WRDS. |
| `CAR205_merge.py` | Drops existing return variables from the master dataset and replaces them with CAR calculated over the [-20, +5] window|
| `regression2.py` | Runs regression on the [-20, +5] window dataset. |
| `CAR205.csv` | Dataset of stock returns calculated in window [-20, +5]|
| `Master_Regression_Dataset_205.csv` | Version of the final dataset replacing the [-1, +1] returns with [-20, +5] returns |
| `WRDS_Event_Study_Input_205.txt` | Text file to request WRDS for the [-20, +5] window returns. |

### Modified Relative Size Regression (Market Cap -50)

| File | Description |
|---|---|
| `merge_1_v2.py` | Filters Zephyr data for 100% takeovers, removes deals within a one-year window, and matches with CRSP data shifted backward by 50 days to extract market cap data. |
| `merge_2_v2.py` | Aligns Day -50 relative size data with CAR data using a forward chronological merge (four-day tolerance) to bridge any calendar gaps. |
| `final_merge_v2.py` | Fixes Zephyr layout issues, filters for US deals, calculates stock percentages, matches industry codes, and applies a log transformation to the Day -50 market cap data. |
| `regression3.py` | Runs OLS regression using the Day -50 adjusted dataset. Cleans entries and prints the summary. |
| `UPDATE_2_Export 08_05_2026 09_45.csv` | Copy of the raw export data from Zephyr |
| `wrds_car_data.csv` | Copy of the CAR spreadsheet from WRDS. |
| `Master_Relative_Size_Data_v2.csv` | Intermediate dataset calculating deal sizes using stock prices from 50 days before announcement.|
| `Final_Event_Study_Merged_v2.csv` | Combined dataset linking the Day -50 modified size data with the stock returns. |
| `Master_Regression_Dataset_v2.csv` | Finalized dataset for the modified relative size robustness check.|

### Visualisation

| File | Description |
|---|---|
| `wrds_car_extraction.py` | Extracts unique acquirer tickers and announcement dates from the master regression dataset, reformats dates, removes duplicates, and generates a WRDS input file. |
| `abret55graph.py` | Processes CAR across the [-5, +5] window to calculate the Average Abnormal Return (AAR) for each day, then generates a line graph to visualize the data. |
| `AAR55_Event_Study_Plot.png` | A line chart showing how AAR changed over the[ -5, +5] window|
| `Master_Regression_Dataset.csv` | A copy of the main finalized dataset|
| `WRDS_Robustness_Input.txt` | A text file used to request the daily abnormal returns for the [-5, +5] window from WRDS. |
| `abret55.csv` | A dataset containing the daily abnormal stock returns in the [-5, +5] window|