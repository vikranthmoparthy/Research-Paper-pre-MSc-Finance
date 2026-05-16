"""
SCRIPT NAME: acquiror_ticker_extractor.py

DESCRIPTION: 
This script extracts acquirer tickers and announcement dates from the final master regression dataset and cleans them.
It renames the columns for WRDS and formats the dates to YYYYMMDD.

INPUTS:
Master_Regression_Dataset.csv

OUTPUTS:
WRDS_Event_Study_Input_205.txt
"""

import pandas as pd

#Load the master regression dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

#Extract ticker and date for single deal
extract = df[['Acquiror ticker symbol', 'Announced date']].copy()

#Remove any rows missing a ticker or date
extract = extract.dropna()

#Clean tickers
extract['Acquiror ticker symbol'] = extract['Acquiror ticker symbol'].astype(str).str.strip().str.upper()

#Format dates to YYYYMMDD
extract['Announced date'] = pd.to_datetime(extract['Announced date']).dt.strftime('%Y%m%d')

#Rename for WRDS compatibility
extract.columns = ['TICKER', 'EVENT_DATE']

#Save as a .txt
extract.to_csv('WRDS_Event_Study_Input_205.txt', sep='\t', index=False)
