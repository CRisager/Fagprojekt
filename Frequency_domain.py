from Split_signals import (plt, np, phy_sections, vir_sections, df_quiz_phy, df_quiz_vir)
# Importing dependencies
import mne

RR = phy_sections[0][0]['RR'] #eksempel på en person

# Convert RR series to a NumPy array - nøvendigt for at at bruge indbygget funktion
RR_data = RR.to_numpy()

# Define bandpass filter parameters
low1 = 0.04  # Low frequency cutoff (Hz)
high1 = 0.15  # High frequency cutoff (Hz)
high2 = 0.4  # High frequency upper cutoff (Hz)
sfreq = 10  # Sampling frequency (Hz), samples per second

# Apply bandpass filter to RR interval data
filtered_rr_low = mne.filter.filter_data(RR_data, sfreq, low1, high1)
filtered_rr_high = mne.filter.filter_data(RR_data, sfreq, high1, high2) 

# Original rr
rr_plot = (RR-np.mean(RR))/np.std(RR)
x_plot = np.arange(0,len(RR))
plt.plot(x_plot, rr_plot)
plt.xlabel("Datapoint")
plt.ylabel("RR")
plt.title("Original RR values")
plt.show()

# low freq rr
x_plot2 = np.arange(0,len(filtered_rr_low))
plt.plot(x_plot2, filtered_rr_low)
plt.xlabel("Datapoint")
plt.ylabel("Filtered RR")
plt.title("Low freq RR values")
plt.show()

# high freq rr
x_plot3 = np.arange(0,len(filtered_rr_high))
plt.plot(x_plot2, filtered_rr_high)
plt.xlabel("Datapoint")
plt.ylabel("Filtered RR")
plt.title("High freq RR values")
plt.show()


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