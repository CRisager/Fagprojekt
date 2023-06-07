from Split_signals import (plt, np, phy_sections, vir_sections, df_quiz_phy, df_quiz_vir)
# Importing dependencies
from IPython.display import Image, Audio
from datetime import datetime
import numpy as np
import scipy.io
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import detrend, welch, windows
from obspy.signal.util import next_pow_2
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, butter, filtfilt
from scipy.interpolate import interp1d
from scipy.signal import detrend
from scipy.fftpack import next_fast_len
import scipy.signal as signal

import mne

RR = phy_sections[0][0]['RR'] #eksempel på en person

# Convert RR series to a NumPy array - nøvendigt for at at bruge indbygget funktion
RR_data = RR.to_numpy()

# Define bandpass filter parameters
lowcut = 0.04  # Low frequency cutoff (Hz)
highcut = 0.4  # High frequency cutoff (Hz)
sfreq = 1000.0  # Sampling frequency (Hz), time is milliseconds

# Apply bandpass filter to RR interval data
filtered_rr = mne.filter.filter_data(RR_data, sfreq, lowcut, highcut)

# Plot the original RR data
plt.figure(figsize=(10, 4))
plt.plot(RR_data, label='Original RR Data')
plt.xlabel('Time')
plt.ylabel('RR Intervals')
plt.title('Original vs Filtered RR Data')
plt.legend()

# Plot the filtered RR data
plt.figure(figsize=(10, 4))
plt.plot(filtered_rr, label='Filtered RR Data')
plt.xlabel('Time')
plt.ylabel('RR Intervals')
plt.title('Original vs Filtered RR Data')
plt.legend()

plt.show()