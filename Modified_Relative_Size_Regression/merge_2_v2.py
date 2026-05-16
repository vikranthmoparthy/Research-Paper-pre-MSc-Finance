"""
SCRIPT NAME: merge2_v2.py

DESCRIPTION: 
This script aligns the adjusted Day -50 relative size data with CAR data using a forward chronological merge with a four-day tolerance.
It bridges calendar gaps to ensure weekend / holiday announcement dates map cleanly to the next available trading day's market returns.

INPUTS:
Master_Relative_Size_Data_v2.csv
wrds_car_data.csv

OUTPUTS:
Final_Event_Study_Merged_v2.csv
"""

import pandas as pd

#Load the CAR data and relative_size .csv
df_original = pd.read_csv('Master_Relative_Size_Data_v2.csv')
df_wrds = pd.read_csv('wrds_car_data.csv')

#Clean the ticker columns so they match perfectly
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

#Drop the redundant ticker column from WRDS to keep it clean
if 'ticker' in final_df.columns:
    final_df = final_df.drop(columns=['ticker'])

#Save the combined dataset
final_df.to_csv('Final_Event_Study_Merged_v2.csv', index=False)

print(final_df[['Acquiror ticker symbol', 'Announced date', 'evtdate', 'car']].head(10))