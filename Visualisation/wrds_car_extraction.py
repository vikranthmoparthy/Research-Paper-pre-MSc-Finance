"""
SCRIPT NAME: wrds_car_extraction.py

DESCRIPTION: 
This script extracts unique acquirer ticker symbols and announcement dates from the final master regression dataset.
It reformats the dates to YYYYMMDD, renames the columns, removes duplicates and generates a input .txt file for WRDS

INPUTS:
Master_Regression_Dataset.csv

OUTPUTS:
WRDS_Robustness_Input.txt
"""

import pandas as pd

#Load final master regression dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

#Extract just the ticker and the announcement date
extract = df[['Acquiror ticker symbol', 'Announced date']].copy()

#Convert the date to the WRDS-required YYYYMMDD format
extract['Announced date'] = pd.to_datetime(extract['Announced date']).dt.strftime('%Y%m%d')

#Rename the columns to be WRDS compatible
extract.columns = ['TICKER', 'EVENT_DATE']

#Drop any potential duplicates to avoid running the same deal twice
extract = extract.drop_duplicates()

#Save the output to a new .txt file for WRDS upload
extract.to_csv('WRDS_Robustness_Input.txt', sep='\t', index=False)