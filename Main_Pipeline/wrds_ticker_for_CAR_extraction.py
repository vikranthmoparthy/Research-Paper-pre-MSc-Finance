"""
SCRIPT NAME: wrds_ticker_for_CAR_extraction.py

DESCRIPTION: 
This script extracts unique acquirer tickers and announcement dates from Master_Relative_Size_Data.csv
It formats the dates to YYYYMMDD and saves the output as a text file formatted for the WRDS Event Study tool.

INPUTS:
Master_Relative_Size_Data.csv

OUTPUTS:
WRDS_Robustness_Input.txt
"""

import pandas as pd

df = pd.read_csv('Master_Relative_Size_Data.csv')

#Extract just the ticker and the announcement date
extract = df[['Acquiror ticker symbol', 'Announced date']].copy()

#Convert the date to the WRDS-required YYYYMMDD format
extract['Announced date'] = pd.to_datetime(extract['Announced date']).dt.strftime('%Y%m%d')

#Rename the columns to be WRDS-compatible
extract.columns = ['TICKER', 'EVENT_DATE']

#Drop any potential duplicates to avoid running the same deal twice
extract = extract.drop_duplicates()

#Save the output to a new .txt file ready for WRDS upload
extract.to_csv('WRDS_Robustness_Input.txt', sep='\t', index=False)