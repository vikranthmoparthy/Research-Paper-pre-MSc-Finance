"""
SCRIPT NAME: winsorize.py

DESCRIPTION:
This script tests whether extreme outliers are driving the main regression results. 
It Winsorizes the CAR variable at the 1% and 99% levels and re-runs the HC3 robust regression.

INPUTS:
Master_Regression_Dataset.csv

OUTPUTS:
Winsorized OLS Regression Summary
"""

import pandas as pd
import statsmodels.formula.api as smf

#Load the Master Dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

#Define the variables needed for the regression
vars_to_use = ['car', 'Relative_Size', 'Percent_Stock', 'Public_Target', 'Same_Industry', 'Log_Acq_Size']

#Clean any remaining missing values
df_clean = df.dropna(subset=vars_to_use).copy()

#Winsorize the CAR at the 1st and 99th percentiles
lower_bound = df_clean['car'].quantile(0.01)
upper_bound = df_clean['car'].quantile(0.99)

print(f"Winsorization Bounds:")
print(f"Capping extreme negative returns below: {lower_bound:.4f}")
print(f"Capping extreme positive returns above: {upper_bound:.4f}\n")

df_clean['car_winsorized'] = df_clean['car'].clip(lower=lower_bound, upper=upper_bound)

#Run the regression on the winsorized dependent variable
model_robust_win = smf.ols(
    'car_winsorized ~ Relative_Size + Percent_Stock + Public_Target + Same_Industry + Log_Acq_Size', 
    data=df_clean
).fit(cov_type='HC3')

print(model_robust_win.summary())