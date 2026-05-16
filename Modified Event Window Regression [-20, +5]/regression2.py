"""
SCRIPT NAME: regression2.py

DESCRIPTION: 
This script executes regression on the [-20, +5] event window dataset.
It drops missing values and prints the output.

INPUTS:
Master_Regression_Dataset_205.csv

OUTPUTS:
OLS regression output
"""

import pandas as pd
import statsmodels.formula.api as smf

#Load the Master Dataset
df = pd.read_csv('Master_Regression_Dataset_205.csv')

#Define the variables needed for the regression
vars_to_use = ['car', 'Relative_Size', 'Percent_Stock', 'Public_Target', 'Same_Industry', 'Log_Acq_Size']

#Clean any remaining missing values
df_clean = df.dropna(subset=vars_to_use)

#Run the regression
model_robust = smf.ols('car ~ Relative_Size + Percent_Stock + Public_Target + Same_Industry + Log_Acq_Size', data=df_clean).fit(cov_type='HC3')

#Print the Output
print(model_robust.summary())