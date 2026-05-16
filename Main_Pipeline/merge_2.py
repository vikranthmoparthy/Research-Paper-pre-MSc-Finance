"""
SCRIPT NAME: merge2.py

DESCRIPTION: 
This script aligns the relative size data with CAR from WRDS using a forward chronological merge with a four-day tolerance window.
It ensures each transaction's announcement date is correctly mapped to its corresponding stock market performance window.

INPUTS:
Master_Relative_Size_Data.csv
wrds_car_data.csv

OUTPUTS:
Final_Event_Study_Merged.csv
"""

import pandas as pd

#Load the CAR data and relative_size .csv
df_original = pd.read_csv('Master_Relative_Size_Data.csv')
df_wrds = pd.read_csv('wrds_car_data.csv')

#Clean the Ticker columns so they match perfectly
df_original['Acquiror ticker symbol'] = df_original['Acquiror ticker symbol'].astype(str).str.strip().str.upper()
df_wrds['ticker'] = df_wrds['ticker'].astype(str).str.strip().str.upper()

#Standardize the Dates into Pandas Datetime format
df_original['Announced date'] = pd.to_datetime(df_original['Announced date'])

df_wrds['evtdate'] = pd.to_datetime(df_wrds['evtdate'], format='%Y-%m-%d')

#Sort both datasets by date, which is required for merge_asof
df_original = df_original.sort_values('Announced date')
df_wrds = df_wrds.sort_values('evtdate')

#Perform the Merge
final_df = pd.merge_asof(
    df_original, 
    df_wrds, 
    left_on='Announced date', 
    right_on='evtdate', 
    left_by='Acquiror ticker symbol',  
    right_by='ticker',                 
    direction='forward',               
    tolerance=pd.Timedelta(days=4)     
)

#dDop the redundant 'ticker' column from WRDS to keep it clean
if 'ticker' in final_df.columns:
    final_df = final_df.drop(columns=['ticker'])

#Save your combined dataset
final_df.to_csv('Final_Event_Study_Merged.csv', index=False)

print(final_df[['Acquiror ticker symbol', 'Announced date', 'evtdate', 'car']].head(10))