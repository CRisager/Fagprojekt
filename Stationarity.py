from Split_signals import (plt, np, phy_sections, vir_sections)
from statsmodels.tsa.stattools import adfuller, kpss
import warnings

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""" Den laver FEJL aaaamen altså"""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Function for testing stationarity
def Stationarity_test(rr):
    rr_norm = (rr-np.mean(rr))/np.std(rr)
    # Perform stationarity tests
    stationarity = []
    # Perform the ADF test
    if adfuller(rr_norm)[1] > 0.05: 
        stationarity.append("non-stationary")
    else:
        stationarity.append("stationary") # p-value = 7.58654334e-07 = stationary
    # Perform the KPSS test
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        if kpss(rr_norm)[1] < 0.05: 
            stationarity.append("non-stationary") # p-value = aprox. 0.01 = non-stationary
        else:
            stationarity.append("stationary") 
    # Perform the PP test
    if adfuller(rr_norm, autolag='AIC', regression='ct')[1] < 0.05: 
        stationarity.append("non-stationary") # p-value = 8.2601133e-08 = non-stationary
    else:
        stationarity.append("stationary")
    # Print whether stationary or not 
    if stationarity.count("stationary") > 1:
        result = "Stationary"
    else:
        result = "Non-stationary"
    return result

stationarity_phy = []
for section in phy_sections:
    print("Section", phy_sections.index(section)+1, "/", len(phy_sections))
    for student in section:
        stationarity_phy.append(Stationarity_test(student["RR"]))
stationarity_vir = []
for section in vir_sections:
    print("Section", vir_sections.index(section)+1, "/", len(vir_sections))
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
        


# Try looking at mean and std in first vs second half
rr = phy_sections[0][0]["RR"]
rr_norm = (rr-np.mean(rr))/np.std(rr)
first_half = rr_norm[:len(rr_norm)//2]
second_half = rr_norm[len(rr_norm)//2:]
print(np.mean(first_half))   # -0.3817
print(np.mean(second_half))  # 0.3816
print(np.std(first_half))    # 1.0204
print(np.std(second_half))   # 0.8169

# Visually examine the signal
x_plot = np.arange(0,len(rr_norm))
fig, ax = plt.subplots(1,1)
plt.plot(x_plot, rr_norm)
plt.title("")
plt.xlabel("Observation")
plt.ylabel("RR_norm")
plt.show()
