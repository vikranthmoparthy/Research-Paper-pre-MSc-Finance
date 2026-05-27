"""
SCRIPT NAME: final_merge.py

DESCRIPTION:
Combines payment rows and keeps only domestic US deals.
Calculates stock payment percentage, identifies public targets, matches industry codes, and builds the final dataset.

INPUTS:
Final_Event_Study_Merged.csv
UPDATE_2_Export 08_05_2026 09_45.csv
csrp_target_data.csv

OUTPUTS:
Master_Regression_Dataset.csv
"""

import pandas as pd
import numpy as np

#Load the datasets
event_study_df = pd.read_csv('Final_Event_Study_Merged.csv')
controls_df = pd.read_csv('UPDATE_2_Export 08_05_2026 09_45.csv')
crsp_target_df = pd.read_csv('csrp_target_data.csv')

#Forward-fill for rows from Orbis dataset and calculate Percent_Stock
controls_df['Deal Number'] = controls_df['Deal Number'].ffill()
controls_df['Deal value th USD'] = controls_df['Deal value th USD'].ffill()

controls_df['Deal method of payment value th USD'] = controls_df['Deal method of payment value th USD'].astype(str).str.replace(',', '', regex=False)
controls_df['Deal method of payment value th USD'] = pd.to_numeric(controls_df['Deal method of payment value th USD'], errors='coerce').fillna(0)
controls_df['Deal value th USD'] = controls_df['Deal value th USD'].astype(str).str.replace(',', '', regex=False)
controls_df['Deal value th USD'] = pd.to_numeric(controls_df['Deal value th USD'], errors='coerce').fillna(1) 

stock_rows = controls_df[controls_df['Deal method of payment'] == 'Shares'].copy()
stock_rows['Percent_Stock'] = stock_rows['Deal method of payment value th USD'] / stock_rows['Deal value th USD']
stock_rows['Percent_Stock'] = stock_rows['Percent_Stock'].clip(upper=1.0)
stock_percentages = stock_rows[['Deal Number', 'Percent_Stock']].drop_duplicates()

controls_main = controls_df.dropna(subset=['Acquiror name']).drop_duplicates(subset=['Deal Number'])
clean_controls = pd.merge(controls_main, stock_percentages, on='Deal Number', how='left')
clean_controls['Percent_Stock'] = clean_controls['Percent_Stock'].fillna(0.0)
clean_controls = clean_controls.drop(columns=['Deal method of payment', 'Deal method of payment value th USD'])

#Ensure a purely US domestic sample
clean_controls['Acquiror country code'] = clean_controls['Acquiror country code'].fillna('US')
clean_controls['Target country code'] = clean_controls['Target country code'].fillna('US')

is_cross_border = (clean_controls['Acquiror country code'] != clean_controls['Target country code'])
cb_count = is_cross_border.sum()
clean_controls = clean_controls[~is_cross_border].copy()

#Create the remaining control variables
crsp_target_df = crsp_target_df.dropna(subset=['Ticker'])
crsp_target_df['DlyCalDt'] = pd.to_datetime(crsp_target_df['DlyCalDt'].astype(str), format='%Y-%m-%d')

#Clean CRSP Tickers
crsp_target_df['Match_Key'] = crsp_target_df['Ticker'].astype(str).str.strip().str.upper() + "_" + crsp_target_df['DlyCalDt'].dt.strftime('%Y-%m-%d')
valid_public_keys = set(crsp_target_df['Match_Key'].unique())

clean_controls['Announced date'] = pd.to_datetime(clean_controls['Announced date'], format='mixed', dayfirst=True)

#Clean Zephyr Tickers and safely create match keys
clean_controls['Target ticker symbol'] = clean_controls['Target ticker symbol'].astype(str).str.strip().str.upper()

#Replace string 'NAN' from astype cast with actual missing values
clean_controls['Target ticker symbol'] = clean_controls['Target ticker symbol'].replace({'NAN': np.nan, 'NONE': np.nan, '': np.nan})

def check_public_target(row):
    #If there is no ticker, it's not a public target
    if pd.isna(row['Target ticker symbol']):
        return 0
    key = str(row['Target ticker symbol']) + "_" + row['Announced date'].strftime('%Y-%m-%d')
    return 1 if key in valid_public_keys else 0

clean_controls['Public_Target'] = clean_controls.apply(check_public_target, axis=1)

#Same Industry NAICS Dummy Variable
clean_controls['Acq_NAICS_2'] = clean_controls['Acquiror primary NAICS 2017 code'].astype(str).str.strip().str.lower().str[:2]
clean_controls['Tar_NAICS_2'] = clean_controls['Target primary NAICS 2017 code'].astype(str).str.strip().str.lower().str[:2]

#Ensure they match and are not the result of a 'nan' or 'na' string
clean_controls['Same_Industry'] = (
    (clean_controls['Acq_NAICS_2'] == clean_controls['Tar_NAICS_2']) & 
    (~clean_controls['Acq_NAICS_2'].isin(['na', 'no', '']))
).astype(int)

#Final merge
final_regression_dataset = pd.merge(
    event_study_df, 
    clean_controls[['Deal Number', 'Percent_Stock', 'Public_Target', 'Same_Industry']], 
    on='Deal Number', 
    how='inner' 
)

final_regression_dataset['Log_Acq_Size'] = np.log(final_regression_dataset['DlyCap'])


#Drop missing CAR values
initial_len = len(final_regression_dataset)
final_regression_dataset = final_regression_dataset.dropna(subset=['car'])
dropped_car = initial_len - len(final_regression_dataset)

#Export Final Dataset
final_regression_dataset.to_csv('Master_Regression_Dataset.csv', index=False)