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



# Test stationarity for all the physical data 
stationarity_list = []
for index, section in enumerate(phy_sections, start=1):
    print("Section", index, "/", len(phy_sections))
    for student in section:
        stationarity_list.append(Stationarity_test(student["RR"]))
# Print whether the physical data is stationary or not
if stationarity_list.count("Stationary") > stationarity_list.count("Non-stationary"):
    physical = "Phy data is stationary"
else:
    physical = "Phy data is non-stationary" 
# The physical data is non-stationary 


############### Use square root to make stationary ###############
stationarity_list = []
for index, section in enumerate(phy_sections, start=1):
    print("Section", index, "/", len(phy_sections))
    for student in section:
        sqrt_rr = [math.sqrt(num) for num in student["RR"]]
        stationarity_list.append(Stationarity_test(sqrt_rr))
# Print whether the physical data is stationary or not
if stationarity_list.count("Stationary") > stationarity_list.count("Non-stationary"):
    physical = "Phy data is stationary"
else:
    physical = "Phy data is non-stationary"
# The data is still non-stationary 


############### Use log to make stationary ###############
stationarity_list = []
for index, section in enumerate(phy_sections, start=1):
    print("Section", index, "/", len(phy_sections))
    for student in section:
        sqrt_rr = [math.log(num) for num in student["RR"]]
        stationarity_list.append(Stationarity_test(sqrt_rr))
# Print whether the physical data is stationary or not
if stationarity_list.count("Stationary") > stationarity_list.count("Non-stationary"):
    physical = "Phy data is stationary"
else:
    physical = "Phy data is non-stationary"
# The data is still non-stationary 


############### Use both to make stationary ###############
stationarity_list = []
for index, section in enumerate(phy_sections, start=1):
    print("Section", index, "/", len(phy_sections))
    for student in section:
        sqrt_rr = [math.log(math.sqrt(num)) for num in student["RR"]]
        stationarity_list.append(Stationarity_test(sqrt_rr))
# Print whether the physical data is stationary or not
if stationarity_list.count("Stationary") > stationarity_list.count("Non-stationary"):
    physical = "Phy data is stationary"
else:
    physical = "Phy data is non-stationary"
# The data is still non-stationary 

    
############### Use detrending to make stationary ###############
from scipy.signal import detrend 
stationarity_list = []
for index, section in enumerate(phy_sections, start=1):
    print("Section", index, "/", len(phy_sections))
    for student in section:
        sqrt_rr = detrend(student["RR"])
        stationarity_list.append(Stationarity_test(sqrt_rr))
# Print whether the physical data is stationary or not
if stationarity_list.count("Stationary") > stationarity_list.count("Non-stationary"):
    physical = "Phy data is stationary"
else:
    physical = "Phy data is non-stationary"



############### Use detrending to make stationary ###############
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










