import pandas as pd

# 1. Load your master dataset and the NEW [-20, +5] WRDS CAR data
df_master = pd.read_csv('Master_Regression_Dataset.csv')
df_new_car = pd.read_csv('CAR205.csv') # Make sure this matches your downloaded file name

# 2. Select only the necessary columns from the new WRDS file
df_new_car = df_new_car[['ticker', 'evtdate', 'cret', 'car', 'bhar', 'nrets_est']]

# 3. Rename 'ticker' to match the master dataset
df_new_car = df_new_car.rename(columns={'ticker': 'Acquiror ticker symbol'})

# 4. Drop the OLD return columns from your master dataset
cols_to_drop = ['cret', 'car', 'bhar', 'nrets_est']
df_master = df_master.drop(columns=cols_to_drop, errors='ignore')

# 5. Merge the new [-20, +5] data into the master dataset
df_updated = pd.merge(
    df_master, 
    df_new_car, 
    on=['Acquiror ticker symbol', 'evtdate'], 
    how='inner'
)

# 6. Save the new robustness dataset!
df_updated.to_csv('Master_Regression_Dataset_205.csv', index=False)

print(f"Original dataset rows: {len(df_master)}")
print(f"Updated robustness dataset rows: {len(df_updated)}")
print("Success! The old CAR values have been replaced with the new [-20, +5] values.")
print("Saved as 'Master_Regression_Dataset_205.csv'")