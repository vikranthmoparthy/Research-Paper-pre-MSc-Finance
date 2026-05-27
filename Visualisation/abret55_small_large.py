"""
SCRIPT NAME: abret55_small_large.py

DESCRIPTION: 
This script processes AAR across a [-5, +5] event window to calculate the Average Abnormal Return (AAR) for each relative trading day.
It categorizes deals into Small and Large targets based on the median relative size from the master dataset.
It then generates a line graph to visualize the overall AAR data alongside the subsamples around the announcement date.

INPUTS:
- abret55.csv
- Master_Regression_Dataset.csv

OUTPUTS:
- AAR55_Event_Study_Plot.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Load Master Dataset
master_df = pd.read_csv('Master_Regression_Dataset.csv')

# alculate the median relative size
median_size = master_df['Relative_Size'].median()

#Categorize into 'Large' (>= median) and 'Small' (< median)
master_df['Target_Size'] = np.where(master_df['Relative_Size'] >= median_size, 'Large', 'Small')

#Create a mapping dataframe using both Ticker and Event Date (uniquely identifies deals)
size_mapping = master_df[['Acquiror ticker symbol', 'evtdate', 'Target_Size']].copy()
size_mapping = size_mapping.rename(columns={'Acquiror ticker symbol': 'TICKER'})
size_mapping['TICKER'] = size_mapping['TICKER'].astype(str).str.upper()

#Ensure evtdate is a standardized datetime object so it merges cleanly
size_mapping['evtdate'] = pd.to_datetime(size_mapping['evtdate'])

#Drop absolute duplicates (in case two identical deals exist on the same day)
size_mapping = size_mapping.drop_duplicates(subset=['TICKER', 'evtdate'])

#Load and Clean Event Study Return Data
df = pd.read_csv('abret55.csv')

#Standardize ticker column name to uppercase (WRDS outputs vary)
if 'ticker' in df.columns:
    df = df.rename(columns={'ticker': 'TICKER'})
df['TICKER'] = df['TICKER'].astype(str).str.upper()

#Ensure evtdate column matches
if 'event_date' in df.columns:
    df = df.rename(columns={'event_date': 'evtdate'})
    
#Standardize WRDS date format to match the master dataset
df['evtdate'] = pd.to_datetime(df['evtdate'].astype(str))

#By merging on both Ticker and Date, we guarantee the daily returns map perfectly to the specific deal that occurred on that day.
df = df.merge(size_mapping, on=['TICKER', 'evtdate'], how='inner')

#Force "evttime" and "abret" to be numbers. Any other text becomes NaN.
df['evttime'] = pd.to_numeric(df['evttime'], errors='coerce')
df['abret'] = pd.to_numeric(df['abret'], errors='coerce')

#Drop NaN rows so the math is correct
df = df.dropna(subset=['evttime', 'abret'])

#Convert evttime to integer so our X-axis plots neatly
df['evttime'] = df['evttime'].astype(int)

#Overall AAR
plot_data_all = df.groupby('evttime')['abret'].mean().reset_index()

#Subsample AARs based on Target Size
plot_data_small = df[df['Target_Size'] == 'Small'].groupby('evttime')['abret'].mean().reset_index()
plot_data_large = df[df['Target_Size'] == 'Large'].groupby('evttime')['abret'].mean().reset_index()

#Generate Plot
plt.figure(figsize=(10, 6))

# Plot the three lines
plt.plot(plot_data_all['evttime'], plot_data_all['abret'], color='black', linewidth=2.5, label='All Deals')
plt.plot(plot_data_large['evttime'], plot_data_large['abret'], color='#d62728', linewidth=1.5, linestyle='--', label='Large Targets')
plt.plot(plot_data_small['evttime'], plot_data_small['abret'], color='#1f77b4', linewidth=1.5, linestyle='-.', label='Small Targets')

#Format the X-axis to explicitly show every single day from -5 to +5
min_day = plot_data_all['evttime'].min()
max_day = plot_data_all['evttime'].max()
plt.xticks(np.arange(min_day, max_day + 1, 1))

#Add light gray dotted grid lines
plt.grid(True, linestyle=':', alpha=0.7, color='gray')

#Remove the top and right borders for a cleaner look
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#Color the left and bottom spines a light gray
ax.spines['left'].set_color('#b0b0b0')
ax.spines['bottom'].set_color('#b0b0b0')

#Labeling
plt.xlabel('Event time (Days relative to announcement)', fontsize=14)
plt.ylabel('Average Abnormal Return (AAR)', fontsize=14) 
plt.title('Daily Average Abnormal Returns [-5, +5]', fontsize=16, fontweight='bold', pad=15)

#Add a horizontal line at Y=0 to easily see positive vs. negative returns
plt.axhline(0, color='black', linewidth=0.8, linestyle='-')

#Add legend to distinguish the lines
plt.legend(frameon=False, fontsize=12, loc='best')

#Save as an image
plt.tight_layout()
plt.savefig('AAR55_Event_Study_Plot.png', dpi=300)

#Display the plot
plt.show()