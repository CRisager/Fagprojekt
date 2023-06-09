from Split_signals import (plt, np, phy_sections, vir_sections, mdates)
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

# Measure the time for phy_sections
start_time = time.time()
Stationarity_test(phy_sections[0][0]["RR"])
end_time = time.time()
one_calculation = end_time - start_time # 0.5802 s
Total_time = one_calculation*(7*32 + 6*18)/60
# it would take approximately 3.2 minutes to run through all the data
# That's too long, let's only look at enough data for 30 sec = 50 student segments in total

# Calculate how many to choose from phy vs vir to be fair
num_physical = int(50 * (7 * 32) / ((7 * 32) + (6 * 18)))
num_virtual = 51 - num_physical # 51 because then it's 33 and 18 respectively, which is nice

# Create a list of all student segments for phy and vir
all_studentsegment_phy = [student for section in phy_sections for student in section]
all_studentsegment_vir = [student for section in vir_sections for student in section]

# Randomly choose student segments from each
phy_selections = random.sample(all_studentsegment_phy, num_physical)
vir_selections = random.sample(all_studentsegment_vir, num_virtual)

# Functions for checking chosen random data and printing stationarity result
def Stationarity_result(selections, state):
    # Test stationarity of the randomly chosen data 
    stationarity_list = []
    for student_index, student in enumerate(selections, start=1):
        print("Student", student_index, "/", len(selections))    
        stationarity_list.append(Stationarity_test(student["RR"]))

    # Print whether the physical data is stationary or not
    if stationarity_list.count("Stationary") > stationarity_list.count("Non-stationary"):
        print(state, "data is stationary")
    else:
        print(state, "data is non-stationary") 

Stationarity_result(phy_selections, state = "Physical") # non-stationary
Stationarity_result(vir_selections, state = "Virtual")  # non-stationary



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
fig, ax = plt.subplots(1,1)
plt.plot(phy_sections[0][0]["Time"], rr_norm)
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.title("Visual examination of stationarity")
plt.xlabel("Time")
plt.ylabel("Normalized RR-intervals")
plt.show()
