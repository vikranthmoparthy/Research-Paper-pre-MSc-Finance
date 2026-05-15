import pandas as pd
import numpy as np
from scipy import stats

# 1. Load your final regression dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

# Drop any missing CAR or Relative Size values
df = df.dropna(subset=['car', 'Relative_Size'])

# 2. Determine the Median Cutoff for Relative Size
median_size = df['Relative_Size'].median()

print(f"=== SPLIT CRITERIA ===")
print(f"Median Relative Size Cutoff: {median_size:.4f}")
print(f"Deals <= {median_size:.4f} are 'Small', Deals > {median_size:.4f} are 'Large'\n")

# 3. Create the two sub-samples
small_df = df[df['Relative_Size'] <= median_size]
large_df = df[df['Relative_Size'] > median_size]

# 4. Comprehensive Statistics Function
def get_comprehensive_stats(data, column='car'):
    series = data[column].dropna()
    n = len(series)
    
    # Basic Stats
    mean = series.mean()
    std = series.std(ddof=1)
    
    # Parametric Significance (T-Test for mean = 0)
    t_stat, t_pval = stats.ttest_1samp(series, 0)
    
    # Distribution / Normality (fisher=False gives raw kurtosis where Normal = 3)
    skewness = stats.skew(series)
    kurtosis = stats.kurtosis(series, fisher=False)
    jb_stat, jb_pval = stats.jarque_bera(series)
    
    # Non-Parametric Tests
    # Sign Test (Binomial test: is proportion of positive CARs different from 50%?)
    positive_count = (series > 0).sum()
    sign_pval = stats.binomtest(positive_count, n, p=0.5).pvalue
    
    # Rank Test (Wilcoxon signed-rank test: is the median CAR different from 0?)
    # Note: If there are exactly zero values, Wilcoxon drops them, so we handle safely.
    non_zero_series = series[series != 0]
    if len(non_zero_series) > 0:
        rank_stat, rank_pval = stats.wilcoxon(non_zero_series)
    else:
        rank_pval = np.nan
    
    # Format the output dict
    return {
        "Number of Events": n,
        "Sample Mean": f"{mean:.6f}",
        "Sample Standard deviation": f"{std:.6f}",
        "T-statistic": f"{t_stat:.4f}",
        "P-value (2 sided)": f"{t_pval:.4e}",
        "Sample skewness": f"{skewness:.4f}",
        "Sample kurtosis": f"{kurtosis:.4f}",
        "JB test statistic": f"{jb_stat:.4f}",
        "JB p-value": f"{jb_pval:.4e}",
        "Sign test p-value": f"{sign_pval:.4e}",
        "Rank test p-value": f"{rank_pval:.4e}"
    }

# 5. Compile the final 3-column table
results = {
    "All Deals": get_comprehensive_stats(df),
    "Small Targets": get_comprehensive_stats(small_df),
    "Large Targets": get_comprehensive_stats(large_df)
}

# Convert to DataFrame for a clean view
results_df = pd.DataFrame(results)

print("=== COMPREHENSIVE CAR STATISTICS BY RELATIVE SIZE ===")
print(results_df)

# Optional: Save to a CSV so you can easily copy/paste into Excel or Word
results_df.to_csv('Target_Size_Descriptives.csv')
print("\nSaved table to 'Target_Size_Descriptives.csv'")