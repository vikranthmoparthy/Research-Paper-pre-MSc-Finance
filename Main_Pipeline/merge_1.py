"""
SCRIPT NAME: merge1.py

DESCRIPTION: 
This script filters raw Zephyr deal data to isolate pure 100% takeovers and removes transactions occurring within one year of each other.
It then merges the filtered deals with CRSP acquirer data from the closest preceding trading day to calculate the relative size of each transaction.

INPUTS:
UPDATE_2_Export 08_05_2026 09_45.csv
csrp_acquiror_data.csv

OUTPUTS:
Master_Relative_Size_Data.csv
"""

import pandas as pd

zephyr = pd.read_csv('UPDATE_2_Export 08_05_2026 09_45.csv')

#Convert the 'Acquired stake' column to numeric, forcing text to NaN
zephyr['Acquired stake (%)'] = pd.to_numeric(zephyr['Acquired stake (%)'], errors='coerce')

#Filter to keep only pure takeovers
zephyr = zephyr[zephyr['Acquired stake (%)'] == 100.0]

#Clean Zephyr Data
zephyr = zephyr.dropna(subset=['Acquiror ticker symbol', 'Deal value th USD', 'Announced date'])
zephyr['Deal value th USD'] = zephyr['Deal value th USD'].astype(str).str.replace(',', '').astype(float)
zephyr['Announced date'] = pd.to_datetime(zephyr['Announced date'], format='mixed', dayfirst=True)

#If two or more deals of the same firm occur within a year from each other, keep only the first of the deals, and drop the rest
def filter_confounding_deals(group):
    #Sort chronologically to ensure we step through time correctly
    group = group.sort_values('Announced date')
    kept_rows = []
    last_kept_date = pd.NaT
    
    for _, row in group.iterrows():
        current_date = row['Announced date']
        if pd.isna(last_kept_date):
            #Always keep the firm's very first deal
            kept_rows.append(True)
            last_kept_date = current_date
        else:
            days_diff = (current_date - last_kept_date).days
            if days_diff > 365:
                #It has been more than a year since the last kept deal, so keep
                kept_rows.append(True)
                last_kept_date = current_date
            else:
                #Too close to the last kept deal, so drop
                kept_rows.append(False)   
    return group[kept_rows]

#Apply the above defined iterative filter to the Zephyr data
zephyr = zephyr.groupby('Acquiror ticker symbol', group_keys=False)[zephyr.columns].apply(filter_confounding_deals)

#Subtract 1 day from the announcement date to ensure we use clean market caps
zephyr['Mkt_Cap_Date'] = zephyr['Announced date'] - pd.Timedelta(days=1)

#Load CRSP Market Cap Data
crsp = pd.read_csv('csrp_acquiror_data.csv')
crsp['DlyCalDt'] = pd.to_datetime(crsp['DlyCalDt'])

#Ensuring no invisible spaces or lowercase letters break the merge
zephyr['Acquiror ticker symbol'] = zephyr['Acquiror ticker symbol'].astype(str).str.strip().str.upper()
crsp['Ticker'] = crsp['Ticker'].astype(str).str.strip().str.upper()

#Preparing column for merge
zephyr = zephyr.sort_values('Mkt_Cap_Date')
crsp = crsp.sort_values('DlyCalDt')

#The final_merge matches nearest previous trading date
merged_data = pd.merge_asof(
    zephyr, 
    crsp, 
    left_on='Mkt_Cap_Date',            
    right_on='DlyCalDt', 
    left_by='Acquiror ticker symbol',  
    right_by='Ticker',                 
    direction='backward'               
)

#Drop any deals where a CRSP match couldn't be found
merged_data = merged_data.dropna(subset=['DlyCap'])

#Calculate Relative Size
merged_data['Relative_Size'] = merged_data['Deal value th USD'] / merged_data['DlyCap']

#Final Cleanup
final_dataset = merged_data[[
    'Deal Number', 'Acquiror ticker symbol', 'Announced date', 
    'Deal value th USD', 'DlyCap', 'Relative_Size'
]]

# Save final master file
final_dataset.to_csv('Master_Relative_Size_Data.csv', index=False)
