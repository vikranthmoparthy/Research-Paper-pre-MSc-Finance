import pandas as pd

#Load Zephyr export
zephyr = pd.read_csv('UPDATE_2_Export 08_05_2026 09_45.csv')

#Extract acquiror tickers: Drop blank rows, get unique values, and convert to string
unique_acquirors = zephyr['Acquiror ticker symbol'].dropna().astype(str).unique()

#Clean up any spaces Zephyr might have added
clean_acq_tickers = sorted([ticker.strip() for ticker in unique_acquirors if ticker.strip() != ''])

#Save to a simple text file
with open('WRDS_Acquiror_Tickers.txt', 'w') as f:
    for ticker in clean_acq_tickers:
        f.write(f"{ticker}\n")

#Extract target tickers (For your 'Public_Target' Dummy)
if 'Target ticker symbol' in zephyr.columns:
    unique_targets = zephyr['Target ticker symbol'].dropna().astype(str).unique()
    clean_tar_tickers = sorted([ticker.strip() for ticker in unique_targets if ticker.strip() != ''])
    
    with open('WRDS_Target_Tickers.txt', 'w') as f:
        for ticker in clean_tar_tickers:
            f.write(f"{ticker}\n")
            