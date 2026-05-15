import pandas as pd

# 1. Load your master regression dataset
df = pd.read_csv('Master_Regression_Dataset.csv')

# 2. Extract every single deal (Ticker + Date)
# We do NOT drop duplicates here because we need every event
extract = df[['Acquiror ticker symbol', 'Announced date']].copy()

# 3. Clean and Format
# Remove any rows missing a ticker or date
extract = extract.dropna()

# Clean Tickers (uppercase and stripped)
extract['Acquiror ticker symbol'] = extract['Acquiror ticker symbol'].astype(str).str.strip().str.upper()

# Format dates to YYYYMMDD (The WRDS standard)
extract['Announced date'] = pd.to_datetime(extract['Announced date']).dt.strftime('%Y%m%d')

# 4. Rename for WRDS compatibility
extract.columns = ['TICKER', 'EVENT_DATE']

# 5. Save as a Tab-Separated file (Best for WRDS upload)
extract.to_csv('WRDS_Event_Study_Input_55.txt', sep='\t', index=False)

print(f"Success! Prepared {len(extract)} events for the robustness check.")
print("File saved as: WRDS_Event_Study_Input_55.txt")