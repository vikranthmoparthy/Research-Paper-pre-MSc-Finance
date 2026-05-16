"""
SCRIPT NAME: CAR205_merge.py

DESCRIPTION: 
This script drops the existing return variables from the master dataset and replaces them with the new CAR calculated over the [-20, +5] window.

INPUTS:
Master_Regression_Dataset.csv
CAR205.csv

OUTPUTS:
Master_Regression_Dataset_205.csv
"""

import pandas as pd

#Load the master dataset and the new [-20, +5] WRDS CAR data
df_master = pd.read_csv('Master_Regression_Dataset.csv')
df_new_car = pd.read_csv('CAR205.csv') # Make sure this matches your downloaded file name

#Select only the necessary columns from the new WRDS file
df_new_car = df_new_car[['ticker', 'evtdate', 'cret', 'car', 'bhar', 'nrets_est']]

#Rename ticker to match the master dataset
df_new_car = df_new_car.rename(columns={'ticker': 'Acquiror ticker symbol'})

#Drop the old return columns from the master dataset
cols_to_drop = ['cret', 'car', 'bhar', 'nrets_est']
df_master = df_master.drop(columns=cols_to_drop, errors='ignore')

#Merge the new [-20, +5] data into the master dataset
df_updated = pd.merge(
    df_master, 
    df_new_car, 
    on=['Acquiror ticker symbol', 'evtdate'], 
    how='inner'
)

#Save the new robustness dataset
df_updated.to_csv('Master_Regression_Dataset_205.csv', index=False)
