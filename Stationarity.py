from Split_signals import (pd, plt, np, phy_sections, vir_sections, mdates, dphy_resampled)
from statsmodels.tsa.stattools import adfuller, kpss
import warnings
from collections import Counter
import statsmodels.api as sm
import math


# Function for testing stationarity
def Stationarity_test(rr):
    rr_norm = (rr-np.mean(rr))/np.std(rr)
    # Perform stationarity tests
    stationarity = []
    # Perform the ADF test
    stationarity.append("non-stationary" if adfuller(rr_norm)[1] > 0.05 else "stationary")
        # example p-value = 7.58654334e-07 = stationary
    # Perform the KPSS test
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        stationarity.append("non-stationary" if kpss(rr_norm)[1] < 0.05 else "stationary")
        # example p-value = aprox. 0.01 = non-stationary
    # Perform the PP test
    stationarity.append("non-stationary" if adfuller(rr_norm, autolag='AIC', regression='ct')[1] > 0.05 else "stationary")
        # example p-value = 8.2601133e-08 = stationary
    
    # Return which stationarity is most common
    result = Counter(stationarity).most_common(1)[0][0]
    return result


# Test stationarity for all the physical data 
stationarity_list = []
for index, section in enumerate(phy_sections, start=1):
    print("Section", index, "/", len(phy_sections))
    for student in section:
        stationarity_list.append(Stationarity_test(student["RR"]))
        print(Stationarity_test(student["RR"]))
# Print whether the physical data is stationary or not
if stationarity_list.count("stationary") > stationarity_list.count("non-stationary"):
    physical = "Phy data is stationary"
else:
    physical = "Phy data is non-stationary" 
print(physical)
# The data is all stationary!



# Test stationarity for all the virtual data 
stationarity_list = []
for index, section in enumerate(vir_sections, start=1):
    print("Section", index, "/", len(vir_sections))
    for student in section:
        stationarity_list.append(Stationarity_test(student["RR"]))
        print(Stationarity_test(student["RR"]))
# Print whether the physical data is stationary or not
if stationarity_list.count("stationary") > stationarity_list.count("non-stationary"):
    virtual = "Vir data is stationary"
else:
    virtual = "Vir data is non-stationary" 
print(virtual)
# The data is all stationary
