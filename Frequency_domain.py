from Split_signals import (plt, np, phy_sections, vir_sections, df_quiz_phy, df_quiz_vir)
# Importing dependencies
import matplotlib.pyplot as plt
import numpy as np


import mne

RR = phy_sections[0][0]['RR'] #eksempel på en person

# Convert RR series to a NumPy array - nøvendigt for at at bruge indbygget funktion
RR_data = RR.to_numpy()

# Define bandpass filter parameters
low1 = 0.04  # Low frequency cutoff (Hz)
low2 = 0.15
high1 = 0.15  # High frequency cutoff (Hz)
high2 = 0.4
sfreq = 10  # Sampling frequency (Hz), samples per second

# Apply bandpass filter to RR interval data
filtered_rr_low = mne.filter.filter_data(RR_data, sfreq, low1, high1)
filtered_rr_high = mne.filter.filter_data(RR_data, sfreq, low1, high2)

# Plot the original RR data
#plt.figure(figsize=(10, 4))
#plt.plot(RR_data, label='Original RR Data')
#plt.xlabel('Time')
#plt.ylabel('RR Intervals')
#plt.title('Original vs Filtered RR Data')
#plt.legend()

# Plot the filtered RR data
#plt.figure(figsize=(10, 4))
#plt.plot(filtered_rr, label='Filtered RR Data')
#plt.xlabel('Time')
#plt.ylabel('RR Intervals')
#plt.title('Original vs Filtered RR Data')
#plt.legend()

#plt.show()