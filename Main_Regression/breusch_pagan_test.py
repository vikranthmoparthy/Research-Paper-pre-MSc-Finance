"""
DESCRIPTION:
This script runs the Breusch-Pagan test for heteroskedasticity on the linear regression for the main event window.

INPUTS:
Master_Regression_Dataset.csv

OUTPUTS:
Lagrange Multiplier (LM) p-value
"""

import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms

#Load the Master Dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

#Define the variables needed for the regression
vars_to_use = ['car', 'Relative_Size', 'Percent_Stock', 'Public_Target', 'Same_Industry', 'Log_Acq_Size']

#Clean any remaining missing values to ensure matrix dimensions match perfectly
df_clean = df.dropna(subset=vars_to_use)

#Run the Standard OLS Regression to get the residuals 
model = smf.ols('car ~ Relative_Size + Percent_Stock + Public_Target + Same_Industry + Log_Acq_Size', data=df_clean).fit()

#Perform the Breusch-Pagan test
bp_test = sms.het_breuschpagan(model.resid, model.model.exog)

#Print only the LM p-value
print(bp_test[1])