"""
SCRIPT NAME: regression.py

DESCRIPTION:
This script runs a the robust linear OLS regression for the main event window
It applies HC3 robust standard errors to account for heteroskedasticity.

INPUTS:
Master_Regression_Dataset.csv

OUTPUTS:
OLS Regression Summary
"""

import pandas as pd
import statsmodels.formula.api as smf

#Load the Master Dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

#Define the variables needed for the regression
vars_to_use = ['car', 'Relative_Size', 'Percent_Stock', 'Public_Target', 'Same_Industry', 'Log_Acq_Size']

#Clean any remaining missing values
df_clean = df.dropna(subset=vars_to_use)

#Run the Multiple Regression with robust standard errors (HC3)
model_robust = smf.ols('car ~ Relative_Size + Percent_Stock + Public_Target + Same_Industry + Log_Acq_Size', data=df_clean).fit(cov_type='HC3')

#Print the Output
print(model_robust.summary())