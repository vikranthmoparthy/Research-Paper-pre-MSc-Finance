import pandas as pd
import statsmodels.formula.api as smf

# 1. Load the Master Dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

# 2. Define the variables we need for the regression
vars_to_use = ['car', 'Relative_Size', 'Percent_Stock', 'Public_Target', 'Same_Industry', 'Log_Acq_Size']

# 3. Clean any remaining missing values
df_clean = df.dropna(subset=vars_to_use)

# 4. Run the Multiple Regression with ROBUST STANDARD ERRORS (HC3)
# Notice the .fit(cov_type='HC3') at the very end
model_robust = smf.ols('car ~ Relative_Size + Percent_Stock + Public_Target + Same_Industry + Log_Acq_Size', data=df_clean).fit(cov_type='HC3')

# 5. Print the Output
print(model_robust.summary())