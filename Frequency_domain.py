from Resampling import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled, Cutting,
                        phy_lecture_start_time, phy_lecture_end_time, vir_lecture_start_time, 
                        vir_lecture_end_time, dphy_students, dvir_students, df_quiz_phy, df_quiz_vir)

from Split_signals import (phy_break_start_time, phy_break_end_time, vir_break_start_time, vir_break_end_time, 
                           phy_length_before_break, phy_length_after_break, vir_length_before_break, vir_length_after_break, 
                           phys_starttime1, phys_starttime2, phys_starttime3, phys_starttime4, phys_endtime4, phys_starttime5, 
                           phys_starttime6, phys_starttime7, phys_endtime7, vir_starttime1, vir_starttime2, vir_endtime2, 
                           vir_starttime3, vir_starttime4, vir_starttime5, vir_starttime6, vir_endtime6)

from Split_signals import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled,
                           dphy_students, dvir_students, phy_sections, vir_sections, df_quiz_phy, df_quiz_vir)

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

RR = phy_sections[0][0]['RR']

# Creating the time stamp
timestamp = np.cumsum(RR)
# Plotting R-R interval prior to interpolation
plt.figure(figsize = (15,7))
plt.plot(timestamp, RR, '-o')

# Interpolate
f = interp1d(timestamp, RR, 'linear')

# Sample rate for interpolation
fs = 10.0
steps = 1 / fs

# Now we can sample from interpolation function
timeindex_inter = np.arange(np.min(timestamp), np.max(timestamp), steps)
rr_interpolated = f(timeindex_inter)

plt.figure(figsize = (15,7))
plt.plot(timestamp, RR)
plt.plot(timeindex_inter, rr_interpolated, 'o')

# Detrend time-series (to remove slow drifts)
rr_interpolated = detrend(rr_interpolated)

# Plotting the power spectrum
nfft = next_pow_2(len(rr_interpolated))
window = windows.hamming(len(rr_interpolated)//4)
freqs, PSD = welch(rr_interpolated, fs=fs, window=window, nfft=nfft, scaling='density', return_onesided=True, detrend=False)

plt.figure(figsize = (15,7))
plt.plot(freqs, PSD)
plt.xlim(0.04,0.4)
#plt.ylim(0, 0.15)
plt.xlabel('Frequency')
plt.ylabel('Power spectrum')
plt.title("FFT Spectrum (Welch's periodogram)")
plt.show()
