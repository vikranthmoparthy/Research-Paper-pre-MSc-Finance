"""
SCRIPT NAME: abret55graph.py

DESCRIPTION: 
This script processes CAR across a [-5, +5] event window to calculate the Average Abnormal Return (AAR) for each relative trading day.
It then generates a line graph to visualize the AAR data around the announcement date.

INPUTS:
abret55.csv

OUTPUTS:
AAR55_Event_Study_Plot.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Load and clean data
df = pd.read_csv('abret55.csv')

#We force "evttime" and "abret" to be numbers. Any other text becomes NaN.
df['evttime'] = pd.to_numeric(df['evttime'], errors='coerce')
df['abret'] = pd.to_numeric(df['abret'], errors='coerce')

#Drop those NaN rows so the math is correct
df = df.dropna(subset=['evttime', 'abret'])

#Convert evttime to integer so our X-axis plots neatly
df['evttime'] = df['evttime'].astype(int)

#Group by the relative event day (-5 to +5) and calculate the mean of abret
plot_data = df.groupby('evttime')['abret'].mean().reset_index()

#Generate plot
plt.figure(figsize=(10, 6))

#Plot the main AAR line
plt.plot(plot_data['evttime'], plot_data['abret'], color='black', linewidth=1.5)

#Format the X-axis to explicitly show every single day from -5 to +5
min_day = plot_data['evttime'].min()
max_day = plot_data['evttime'].max()
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
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')

#Save as an image
plt.tight_layout()
plt.savefig('AAR55_Event_Study_Plot.png', dpi=300)

#Display the plot
plt.show()