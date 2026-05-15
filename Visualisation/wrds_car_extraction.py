import pandas as pd

# 1. Load your final master regression dataset
# (Replace with your actual filename if it's slightly different)
df = pd.read_csv('Master_Regression_Dataset.csv')

# 2. Extract just the ticker and the announcement date
extract = df[['Acquiror ticker symbol', 'Announced date']].copy()

# 3. Convert the date to the WRDS-required YYYYMMDD format
extract['Announced date'] = pd.to_datetime(extract['Announced date']).dt.strftime('%Y%m%d')

# 4. Rename the columns to be simple and WRDS-friendly
extract.columns = ['TICKER', 'EVENT_DATE']

# 5. Drop any potential duplicates to avoid running the same deal twice
extract = extract.drop_duplicates()

# 6. Save the output to a new .txt file ready for WRDS upload
# We use to_csv but change the extension to .txt and use a tab separator (sep='\t')
extract.to_csv('WRDS_Robustness_Input.txt', sep='\t', index=False)

print("Extraction complete! Your file 'WRDS_Robustness_Input.txt' is ready for WRDS.")
print("\nHere is a preview of the new format:")
print(extract.head())