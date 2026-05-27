"""
SCRIPT NAME: update_descriptive_statistics_explanatory_variables.py

DESCRIPTION:
Separates the master dataset into small and large samples based on median relative deal size. 
Calculates relevant descriptive and distributional statistics for all explanatory variables.

INPUTS:
Master_Regression_Dataset.csv

OUTPUTS:
Explanatory_Descriptives.csv
"""
import pandas as pd
from scipy import stats

#Load final regression dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

#Define explanatory variables
exp_vars = ['Relative_Size', 'Percent_Stock', 'Public_Target', 'Same_Industry', 'Log_Acq_Size']

#Drop any missing values to ensure a consistent sample
df = df.dropna(subset=['car'] + exp_vars)

#Determine the Median Cutoff for Relative Size
median_size = df['Relative_Size'].median()
print(f"Median Relative Size Cutoff: {median_size:.4f}")

#Create the two sub-samples
small_df = df[df['Relative_Size'] <= median_size]
large_df = df[df['Relative_Size'] > median_size]

#Function for universally applicable statistics
def get_applicable_stats(series):
    series = series.dropna()
    n = len(series)
    
    if n == 0:
        return {}

    #Calculate statistics
    mean = series.mean()
    std = series.std(ddof=1)
    skewness = stats.skew(series)
    kurtosis = stats.kurtosis(series, fisher=False)
    jb_stat, jb_pval = stats.jarque_bera(series)
    
    #Format the output dict
    return {
        "Number of Events": n,
        "Sample Mean": f"{mean:.6f}",
        "Sample Standard deviation": f"{std:.6f}",
        "Sample skewness": f"{skewness:.4f}",
        "Sample kurtosis": f"{kurtosis:.4f}",
        "JB test statistic": f"{jb_stat:.4f}",
        "JB p-value": f"{jb_pval:.4e}"
    }

#Compile results for all variables
all_results = {}

for var in exp_vars:
    #Create a DataFrame for each variable comparing the three groups
    var_results = {
        "All Deals": get_applicable_stats(df[var]),
        "Small Targets": get_applicable_stats(small_df[var]),
        "Large Targets": get_applicable_stats(large_df[var])
    }
    all_results[var] = pd.DataFrame(var_results)

#Concatenate all the variable DataFrames into one large summary table
final_df = pd.concat(all_results.values(), axis=1, keys=all_results.keys())

#Save to a CSV
final_df.to_csv('Explanatory_Descriptives.csv')