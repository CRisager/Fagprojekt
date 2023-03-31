import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import datetime
import pytz

### Working Directory for physical ###
# Path for Chelina = "C:/Users/cheli/OneDrive/Skrivebord/Fagprojekt/Fagprojekt_data/physical"
# Path for Andrea = "/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data/physical"
path = "/Users/jesperberglund/Downloads/HR_Data/physical"
os.chdir(path)

# Using list comprehension to loop over all files in folder
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

# Load all CSV files from physical lecture into a dictionary of DataFrames
data_frames_physical = []
for file in csv_files:
    file_path = os.path.join(path, file)
    df = pd.read_csv(file_path, skiprows=2, sep=";")
    data_frames_physical.append(df)

start_times_physical = []
for file in csv_files:
    file_path = os.path.join(path, file)
    st = pd.read_csv(file_path, skiprows=1, nrows=0, sep=";").columns.values
    st_str = st.item()
    st_str = st.item().split(': ')[1]
    st_datetime = pd.to_datetime(st_str, dayfirst=True)
    start_times_physical.append(st_datetime)
for i in range(len(start_times_physical)):
    print(start_times_physical[i])

### ------------------------------------------------------------------------------------ ###

### Working Directory for virtual ###
# Path for Chelina = "C:/Users/cheli/OneDrive/Skrivebord/Fagprojekt/Fagprojekt_data/virtual"
# Path for Andrea = "/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data/virtual"
path = "/Users/jesperberglund/Downloads/HR_Data/virtual"
os.chdir(path)
# Using list comprehension to loop over all files in folder
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

# Load all CSV files from physical lecture into a dictionary of DataFrames
data_frames_virtual = []
for file in csv_files:
    file_path = os.path.join(path, file)
    df = pd.read_csv(file_path, skiprows=2, sep=";")
    data_frames_virtual.append(df)

# Access a specific DataFrame by filename
print(data_frames_virtual[0].iloc[0])

for file in data_frames_physical:
    print(file.iloc[0])



Ch_start = pd.to_datetime(["21-03-2023 10:48:21"], dayfirst=True)
Tch_start = pd.to_datetime(["21-03-2023 10:48:38"], dayfirst=True)

d = [Ch_data, Tch_data]
starts = [Ch_start, Tch_start]
for i in range(len(d)):
    d0 = d[i]
    d0 = d0.drop("Unnamed: 3", axis=1)
    # Ensure the corrected and non-corrected accounts for all data
    RR = np.cumsum(d0["RR"])
    cRR = np.cumsum(d0["Artifact corrected RR"])
    if np.nanmax(RR) != np.nanmax(cRR):
        print("The cumulative times are not the same for corrected and uncorrected")
        print(f"For subject {i}, there is a difference of {np.nanmax(RR)-np.nanmax(cRR)}")
    # Drop rows with NaN, due to dissimilar number of "R-R" recordings due to artifacts
    d0 = d0.dropna()
    # Compute new cRR without NaN
    cRR = np.cumsum(d0["Artifact corrected RR"])
    s0 = starts[i]
    Time = [pd.to_datetime(s0.to_pydatetime() + datetime.timedelta(seconds=i/1000))[0] for i in cRR]
    d0["Time"] = Time
    # Calculate Heart Rate pr. min (bpm) from the R-R intervals
    bpm = 60/(d0["Artifact corrected RR"]/1000)
    d0["Heart Rate"] = bpm
    d[i] = d0

# Plot with the actual times
fig, ax = plt.subplots(1,1)
sns.lineplot(data = d[0], x="Time", y="Artifact corrected RR", color = "red")
sns.lineplot(data = d[1], x="Time", y="Artifact corrected RR", color = "blue")
plt.title("Artifact Corrected RR")

# With the actual dots
fig, ax = plt.subplots(1,1)
sns.scatterplot(data = d[0], x="Time", y="Artifact corrected RR", color = "red",
                alpha=0.5)
sns.scatterplot(data = d[1], x="Time", y="Artifact corrected RR", color = "blue",
                alpha=0.5)
plt.title("Artifact Corrected RR")

# Non-corrected raw data
fig, ax = plt.subplots(1,1)
sns.lineplot(data = d[0], x="Time", y="RR", color = "red")
sns.lineplot(data = d[1], x="Time", y="RR", color = "blue")
plt.title("Raw RR")

# Heart rate
fig, ax = plt.subplots(1,1)
sns.lineplot(data = d[0], x="Time", y="Heart Rate", color = "red")
sns.lineplot(data = d[1], x="Time", y="Heart Rate", color = "blue")
plt.title("BPM based on corrected RR")

# They are misaligned
# Interpolation and resampling at common time points
# Convert times to float timestamps
Ch_timestamps = [pd.Timestamp(ele).timestamp() for ele in d[0]["Time"]]
Tch_timestamps = [pd.Timestamp(ele).timestamp() for ele in d[1]["Time"]]
# Round to nearest second and get the common timepoints between the two timeseries
common_timestamps = np.intersect1d(np.round(Ch_timestamps,0),np.round(Tch_timestamps,0))
# Remove the first and last timepoint in case of rounding up or down
common_timestamps = common_timestamps[1:-1]
# Upsample to sfreq of interest
sfreq = 10
max_diff = int(common_timestamps[-1]-common_timestamps[0])
upsampled_timestamps = np.linspace(common_timestamps[0],common_timestamps[-1],(sfreq*max_diff)+1)

# Take into account Daylight Saving time and the timezone from UTC
upsampled_datetimes = [datetime.datetime.fromtimestamp(ele-60*60) for ele in upsampled_timestamps]

# Fit function for linear interpolation
Chf = scipy.interpolate.interp1d(Ch_timestamps,d[0]["Artifact corrected RR"], kind="linear")
Tchf = scipy.interpolate.interp1d(Tch_timestamps,d[1]["Artifact corrected RR"], kind="linear")
# Interpolate to common timestamps
Ch_interp = Chf(upsampled_timestamps)
Tch_interp = Tchf(upsampled_timestamps)

# Plot the resampled data at the common timestamps
resampled_df = pd.DataFrame({"Chelina_cRR":Ch_interp,"Tch_cRR":Tch_interp,
                             "Time":upsampled_datetimes})
# Plot with the actual times
fig, ax = plt.subplots(1,1)
sns.lineplot(data = resampled_df, x="Time", y="Chelina_cRR", color = "red")
sns.lineplot(data = resampled_df, x="Time", y="Tch_cRR", color = "blue")
plt.title("Resampled aligned Artifact Corrected RR")

# With dots
fig, ax = plt.subplots(1,1)
sns.scatterplot(data = resampled_df, x="Time", y="Chelina_cRR", color = "red")
sns.scatterplot(data = resampled_df, x="Time", y="Tch_cRR", color = "blue")
plt.title("Resampled aligned Artifact Corrected RR")




### Cross-correlation with scipy
norm_Ch_interp = (Ch_interp-np.mean(Ch_interp))/np.std(Ch_interp)
norm_Tch_interp = (Tch_interp-np.mean(Tch_interp))/np.std(Tch_interp)

cross_corr = scipy.signal.correlate(norm_Ch_interp, norm_Tch_interp, mode="full")
cross_corr /= len(cross_corr)
delays = np.linspace(-(len(Ch_interp)-1),len(Ch_interp)-1,len(cross_corr))
fig, ax = plt.subplots(1,1)
plt.plot(delays, cross_corr)

print(delays[np.argmax(cross_corr)])
