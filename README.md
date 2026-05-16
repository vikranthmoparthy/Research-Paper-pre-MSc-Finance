M&A Event Study Empirical Pipeline


1. Repository Map

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
├── Main_Regression
│   ├── Master_Regression_Dataset.csv
│   ├── Target_Size_Descriptives.csv
│   ├── regression.py
│   └── update_descriptive_statistics.py
├── Modified_Event_Window_Regression
│   ├── CAR205.csv
│   ├── CAR205_merge.py
│   ├── Master_Regression_Dataset.csv
│   ├── Master_Regression_Dataset_205.csv
│   ├── WRDS_Event_Study_Input_205.txt
│   ├── acquiror_ticker_extractor.py
│   └── regression2.py
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
└── Visualisation
    ├── AAR55_Event_Study_Plot.png
    ├── Master_Regression_Dataset.csv
    ├── WRDS_Robustness_Input.txt
    ├── abret55.csv
    ├── abret55graph.py
    └── wrds_car_extraction.py


2. Running Instructions

To run the analysis, execute the Python scripts in the following order within their respective folders:

Main_Pipeline
1. Run extract_acquiror_target_ticker.py to generate the ticker lists for WRDS.
2. Run merge_1.py to filter the deals and calculate the initial relative sizes.
3. Run wrds_ticker_for_CAR_extraction.py to create the input file needed to download your return data.
4. (Download wrds_car_data.csv from WRDS and place it in the folder)
5. Run merge_2.py to merge the deal sizes with the WRDS return data.
6. Run final_merge.py to assemble the finalized dataset.

Main_Regression
1. Run regression.py to execute the primary statistical model.
2. Run update_descriptive_statistics.py to generate the summary statistics table.

Modified_Event_Window_Regression
1. Run acquiror_ticker_extractor.py to generate the list needed to download the longer-window returns.
2. (Download CAR205.csv from WRDS and place it in the folder)
3. Run CAR205_merge.py to merge the extended-window returns into the dataset.
4. Run regression2.py to execute the robustness check.

Modified_Relative_Size_Regression
1. Run merge_1_v2.py to calculate relative sizes using stock prices from Day -50.
2. Run merge_2_v2.py to merge these new sizes with the CAR data.
3. Run final_merge_v2.py to build the robustness dataset.
4. Run regression3.py to execute the Day -50 regression model.

Visualisation
1. Run wrds_car_extraction.py to create the WRDS input list for daily returns.
2. (Download abret55.csv from WRDS and place it in the folder)
3. Run abret55graph.py to generate the visual plot of the stock returns.


3. File Descriptions
--------------------

Main_Pipeline Folder
- extract_acquiror_target_ticker.py: This script extracts unique acquirer and target ticker symbols from the Zephyr deal export. It removes empty entries, cleans whitespace, sorts the tickers alphabetically, and saves them into separate text files for WRDS data queries.
- merge_1.py: This script filters raw Zephyr deal data to isolate pure 100% takeovers and removes transactions occurring within one year of each other. It then merges the filtered deals with CRSP acquirer data from the closest preceding trading day to calculate the relative size of each transaction.
- merge_2.py: This script aligns the relative size data with CAR from WRDS using a forward chronological merge with a four-day tolerance window. It ensures each transaction's announcement date is correctly mapped to its corresponding stock market performance window.
- final_merge.py: This script fixes Zephyr's multi-row layout by combining separate payment rows and filters the data to keep only domestic US deals. It then calculates the stock payment percentage, identifies public targets, matches industry codes, and builds the final dataset for regression.
- wrds_ticker_for_CAR_extraction.py: This script extracts unique acquirer tickers and announcement dates from Master_Relative_Size_Data.csv It formats the dates to YYYYMMDD and saves the output as a text file formatted for the WRDS Event Study tool.
- .DS_Store: A system file created by macOS to store custom attributes of its containing folder.
- UPDATE_2_Export 08_05_2026 09_45.csv: The raw export data from Zephyr containing the initial list of M&A deals.
- wrds_car_data.csv: A spreadsheet containing the cumulative abnormal returns for the companies involved in the deals, sourced from WRDS.
- Master_Relative_Size_Data.csv: An intermediate dataset that stores the calculated relative sizes of the deals before adding the return data.
- Final_Event_Study_Merged.csv: A combined dataset merging the relative size deal data with the WRDS stock return data.
- Master_Regression_Dataset.csv: The finalized, fully clean dataset containing all variables needed to run the main statistical regressions.
- WRDS_Acquiror_Tickers.txt: A text file containing a clean list of the acquirers' stock tickers to be uploaded to WRDS.
- WRDS_Target_Tickers.txt: A text file containing a clean list of the targets' stock tickers to be uploaded to WRDS.
- WRDS_Robustness_Input.txt: A text file linking acquirer tickers with their specific event dates, used to pull targeted return data from WRDS.

Main_Regression Folder
- regression.py: This script runs a the robust linear OLS regression for the main event window It applies HC3 robust standard errors to account for heteroskedasticity.
- update_descriptive_statistics.py: This script separates the master dataset into small and large target subsamples based on the median relative deal size. It then calculates descriptive statistics and runs both parametric and non-parametric significance tests on the CAR for each group.
- Master_Regression_Dataset.csv: A copy of the finalized, clean dataset used to run the main statistical model.
- Target_Size_Descriptives.csv: A table summarizing the statistical properties of the deals, split by whether the target company was large or small.

Modified_Event_Window_Regression Folder
- acquiror_ticker_extractor.py: This script extracts acquirer tickers and announcement dates from the final master regression dataset and cleans them. It renames the columns for WRDS and formats the dates to YYYYMMDD.
- CAR205_merge.py: This script drops the existing return variables from the master dataset and replaces them with the new CAR calculated over the [-20, +5] window. It uses an inner join on ticker and event date to build the updated dataset.
- regression2.py: This script executes regression using the [-20, +5] event window dataset. It drops missing values, applies HC3 robust standard errors, and prints the output.
- CAR205.csv: A dataset of stock returns calculated over a longer 26-day window to check for early market rumors.
- Master_Regression_Dataset.csv: A copy of the standard master dataset used as a base before adding the new extended returns.
- Master_Regression_Dataset_205.csv: A version of the final dataset that replaces the standard return window with the extended 26-day return window.
- WRDS_Event_Study_Input_205.txt: A text file used to query WRDS specifically for the extended 26-day event window returns.

Modified_Relative_Size_Regression Folder
- merge_1_v2.py: This script filters raw Zephyr deal data to isolate 100% takeovers and removes deals from the same acquiror occurring within a one-year window. It then matches these deals with CRSP acquirer data shifted backward by 50 trading days to extract market capitalization data.
- merge_2_v2.py: This script aligns the adjusted Day -50 relative size data with CAR data using a forward chronological merge with a four-day tolerance. It bridges calendar gaps to ensure weekend / holiday announcement dates map cleanly to the next available trading day's market returns.
- final_merge_v2.py: This script fixes Zephyr's multi-row layout by combining separate payment rows and filters the data to keep only domestic US deals. It calculates the stock payment percentage, identifies public targets, matches industry codes, and applies a log transformation to the Day -50 market capitalization data to build the final dataset for the regression.
- regression3.py: This script runs the OLS regression using the Day -50 market capitalization adjusted dataset. It cleans missing entries, applies HC3 robust standard errors, and prints the final model summary.
- UPDATE_2_Export 08_05_2026 09_45.csv: A copy of the raw export data from Zephyr used to build the modified Day -50 dataset.
- Wrds_car_data.csv: A copy of the standard cumulative abnormal returns spreadsheet sourced from WRDS.
- Master_Relative_Size_Data_v2.csv: A modified intermediate dataset where the deal sizes are calculated using stock prices from 50 days before the announcement.
- Final_Event_Study_Merged_v2.csv: A combined dataset that links the Day -50 modified size data with the stock returns.
- Master_Regression_Dataset_v2.csv: The finalized dataset built specifically to test if measuring company size 50 days early changes the regression results.

Visualisation Folder
- wrds_car_extraction.py: This script extracts unique acquirer ticker symbols and announcement dates from the final master regression dataset. It reformats the dates to YYYYMMDD, renames the columns, removes duplicates and generates a input .txt file for WRDS.
- abret55graph.py: This script processes CAR across a [-5, +5] event window to calculate the Average Abnormal Return (AAR) for each relative trading day. It then generates a line graph to visualize the AAR data around the announcement date.
- AAR55_Event_Study_Plot.png: An image of a line chart showing how the stock returns trended over the 11-day event window.
- Master_Regression_Dataset.csv: A copy of the finalized dataset used to generate the ticker input file.
- WRDS_Robustness_Input.txt: A text file used to pull the daily abnormal returns for the 11-day window from WRDS.
- abret55.csv: A dataset containing the daily abnormal stock returns for the 11 days right around the deal announcement.