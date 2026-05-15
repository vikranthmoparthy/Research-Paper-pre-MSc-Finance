import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =====================================================================
# 1. LOAD AND CLEAN THE DATA
# =====================================================================
# Replace 'abret55.csv' with the actual name of your WRDS file
df = pd.read_csv('abret55.csv')

# Clean the data: WRDS sometimes includes weird error rows (like the '.-.' row).
# We force 'evttime' and 'abret' to be numbers. Any garbage text becomes NaN.
df['evttime'] = pd.to_numeric(df['evttime'], errors='coerce')
df['abret'] = pd.to_numeric(df['abret'], errors='coerce')

# Drop those NaN rows so our math is perfectly clean
df = df.dropna(subset=['evttime', 'abret'])

# Convert evttime to integer so our X-axis plots neatly (-5, -4, etc.)
df['evttime'] = df['evttime'].astype(int)

# =====================================================================
# 2. CALCULATE THE AVERAGE ABNORMAL RETURN (AAR)
# =====================================================================
# Group by the relative event day (-5 to +5) and calculate the mean of 'abret'
plot_data = df.groupby('evttime')['abret'].mean().reset_index()

# =====================================================================
# 3. GENERATE THE ACADEMIC-STYLE PLOT
# =====================================================================
plt.figure(figsize=(10, 6))

# Plot the main AAR line (black, sharp)
plt.plot(plot_data['evttime'], plot_data['abret'], color='black', linewidth=1.5)

# Format the X-axis to explicitly show every single day from -5 to +5
min_day = plot_data['evttime'].min()
max_day = plot_data['evttime'].max()
plt.xticks(np.arange(min_day, max_day + 1, 1))

# Add light gray dotted grid lines (matches the standard academic style)
plt.grid(True, linestyle=':', alpha=0.7, color='gray')

# Remove the top and right borders for that clean Stata/paper look
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Color the left and bottom spines a light gray
ax.spines['left'].set_color('#b0b0b0')
ax.spines['bottom'].set_color('#b0b0b0')

# Labeling
plt.xlabel('Event time (Days relative to announcement)', fontsize=14)
plt.ylabel('Average Abnormal Return (AAR)', fontsize=14) 
plt.title('Daily Average Abnormal Returns [-5, +5]', fontsize=16, fontweight='bold', pad=15)

# Add a subtle horizontal line at Y=0 to easily see positive vs. negative returns
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')

# Ensure the layout is tight and save it as a high-quality image
plt.tight_layout()
plt.savefig('CAR55_Event_Study_Plot.png', dpi=300)

print("Plot generated successfully and saved as 'CAR55_Event_Study_Plot.png'")

# Display the plot
plt.show()