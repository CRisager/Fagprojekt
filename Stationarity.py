from Split_signals import (plt, np, phy_sections, vir_sections, mdates, dphy_resampled)
from statsmodels.tsa.stattools import adfuller, kpss
import warnings
from collections import Counter


# Function for testing stationarity
def Stationarity_test(rr):
    rr_norm = (rr-np.mean(rr))/np.std(rr)
    # Perform stationarity tests
    stationarity = []
    # Perform the ADF test
    stationarity.append("non-stationary" if adfuller(rr_norm)[1] > 0.05 else "stationary")
        # p-value = 7.58654334e-07 = stationary
    # Perform the KPSS test
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        stationarity.append("non-stationary" if kpss(rr_norm)[1] < 0.05 else "stationary")
        # p-value = aprox. 0.01 = non-stationary
    # Perform the PP test
    stationarity.append("non-stationary" if adfuller(rr_norm, autolag='AIC', regression='ct')[1] < 0.05 else "stationary")
        # p-value = 8.2601133e-08 = non-stationary
    
    # Return which stationarity is most common
    result = Counter(stationarity).most_common(1)[0][0]
    return result

""" 
###### checking stationarity of all data ######
stationarity_phy = []
for section_index, section in enumerate(phy_sections, start=1):
    print("Section", section_index, "/", len(phy_sections))
    for student in section:
        stationarity_phy.append(Stationarity_test(student["RR"]))
stationarity_vir = []
for section_index, section in enumerate(vir_sections, start=1):
    print("Section", section_index, "/", len(vir_sections))
    for student in section:
        stationarity_vir.append(Stationarity_test(student["RR"]))

if stationarity_phy.count("Stationary") > stationarity_phy.count("Non-stationary"):
    print("Physical data is stationary")
else:
    print("Physical data is non-stationary")
    
if stationarity_vir.count("Stationary") > stationarity_vir.count("Non-stationary"):
    print("Virtual data is stationary")
else:
    print("Virtual data is non-stationary")
"""
####
import time
import random

# Measure the time for one entire signal
start_time = time.time()
Stationarity_test(dphy_resampled[0]["RR"])
end_time = time.time()
print(end_time - start_time) # 36.9 s -> 20 min for hele dphy_resamled


# Measure the time for phy_sections
start_time = time.time()
Stationarity_test(phy_sections[0][0]["RR"])
end_time = time.time()
one_calculation = end_time - start_time # 0.5802 s
Total_time = one_calculation*(7*32 + 6*18)/60
# it would take approximately 3.2 minutes to run through all the data:

stationarity_list = []
for index, section in enumerate(phy_sections, start=1):
    print("Section", index, "/", len(phy_sections))
    for student in section:
        stationarity_list.append(Stationarity_test(student["RR"]))
# Print whether the physical data is stationary or not
if stationarity_list.count("Stationary") > stationarity_list.count("Non-stationary"):
    print("Phy data is stationary")
else:
    print("Phy data is non-stationary") # jup...
    
############### detrending #############

stationarity_list = []
for index, section in enumerate(phy_sections, start=1):
    print("Section", index, "/", len(phy_sections))
    for student in section:
        # Create a DataFrame with the time series data
        df = pd.DataFrame({'time': student["Time"], 'rr_intervals': student["RR"]})
        # Fit a linear regression model to detrend the data
        X = sm.add_constant(np.arange(len(df)))  # Add a constant term to the model
        model = sm.OLS(df['rr_intervals'], X)
        results = model.fit()
        detrended = df['rr_intervals'] - results.fittedvalues
        stationarity_list.append(Stationarity_test(detrended))
# Print whether the physical data is stationary or not
if stationarity_list.count("Stationary") > stationarity_list.count("Non-stationary"):
    print("Phy data is stationary")
else:
    print("Phy data is non-stationary") # jup..

###################### manually test ########################

# Try looking at mean and std in first vs second half
rr = phy_sections[0][0]["RR"]
rr_norm = (rr-np.mean(rr))/np.std(rr)
first_half = rr_norm[:len(rr_norm)//2]
second_half = rr_norm[len(rr_norm)//2:]
print(np.mean(first_half))   # -0.3817
print(np.mean(second_half))  # 0.3816    # diff = 0.7633
print(np.std(first_half))    # 1.0204
print(np.std(second_half))   # 0.8169    # diff = 0.2035
# They change less than 1 but is that enough to assume stationarity?


# Visually examine the signal
rr_norm = (dphy_resampled[0]["RR"] - np.mean(dphy_resampled[0]["RR"]))/np.std(dphy_resampled[0]["RR"])
fig, ax = plt.subplots(1,1)
plt.plot(dphy_resampled[0]["Time"], rr_norm)
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.title("Visual examination of stationarity")
plt.xlabel("Time")
plt.ylabel("Normalized RR-intervals")
plt.show()


###### detredning test and plot #########

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

print(phy_sections[0][0]["Time"])

# Create a DataFrame with the time series data
df = pd.DataFrame({'time': phy_sections[0][0]["Time"], 'rr_intervals': phy_sections[0][0]["RR"]})
# Fit a linear regression model to detrend the data
X = sm.add_constant(np.arange(len(df)))  # Add a constant term to the model
model = sm.OLS(df['rr_intervals'], X)
results = model.fit()
detrended = df['rr_intervals'] - results.fittedvalues
print(Stationarity_test(detrended))

# Plot the original and detrended RR-intervals
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['rr_intervals'], label='Original')
plt.plot(df['time'], detrended, label='Detrended')
plt.xlabel('Time')
plt.ylabel('RR-Intervals')
plt.legend()
plt.show()







