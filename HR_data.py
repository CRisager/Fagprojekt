import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import datetime
import pytz

### ------------------------------------------------------------------------------------ ### 
### Working Directory for physical ###
path = "C:/Users/cheli/OneDrive/Skrivebord/Fagprojekt/Fagprojekt_data/physical"
# path = = "/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data/physical"
#path = "/Users/jesperberglund/Downloads/HR_Data/physical"
os.chdir(path)

# Using list comprehension to loop over all files in folder
csv_files_physical = [f for f in os.listdir(path) if f.endswith('.csv')]

# Load all CSV files from physical lecture into list of data frames
data_frames_physical = []
for file in csv_files_physical:
    file_path = os.path.join(path, file)
    df = pd.read_csv(file_path, skiprows=2, sep=";")
    data_frames_physical.append(df)

start_times_physical = []
for file in csv_files_physical:
    file_path = os.path.join(path, file)
    start_time = pd.read_csv(file_path, skiprows=1, nrows=0, sep=";").columns[0].split(": ")[1]
    start_time = datetime.datetime.strptime(start_time, "%d.%m.%Y %H:%M:%S")
    start_times_physical.append(start_time)
    
### ------------------------------------------------------------------------------------ ###
### Working Directory for virtual ###

path = "C:/Users/cheli/OneDrive/Skrivebord/Fagprojekt/Fagprojekt_data/virtual"
# path = "/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data/virtual"
# path = "/Users/jesperberglund/Downloads/HR_Data/virtual"
os.chdir(path)
# Using list comprehension to loop over all files in folder
csv_files_virtual = [f for f in os.listdir(path) if f.endswith('.csv')]

# Load all CSV files from physical lecture into list of data frames
data_frames_virtual = []
for file in csv_files_virtual:
    file_path = os.path.join(path, file)
    df = pd.read_csv(file_path, skiprows=2, sep=";")
    data_frames_virtual.append(df)

start_times_virtual = []
for file in csv_files_virtual:
    file_path = os.path.join(path, file)
    start_time = pd.read_csv(file_path, skiprows=1, nrows=0, sep=";").columns[0].split(": ")[1]
    start_time = datetime.datetime.strptime(start_time, "%d.%m.%Y %H:%M:%S")
    start_times_virtual.append(start_time)
    
### ------------------------------------------------------------------------------------ ###
### Update "physical" data frame with time stamps and beats per minute

dphy = data_frames_physical 
starts = start_times_physical
for i in range(len(dphy)):
    d0 = dphy[i]
    d0 = d0.drop("Unnamed: 3", axis=1) # Drop empty column
    # Ensure the corrected and non-corrected accounts for all data
    RR = np.cumsum(d0["RR"])
    cRR = np.cumsum(d0["Artifact corrected RR"])
    if np.nanmax(RR) != np.nanmax(cRR):
        print("The cumulative times are not the same for corrected and uncorrected")
        print(f"For subject {i}, there is a difference of {np.nanmax(RR)-np.nanmax(cRR)}")
    # Drop rows with NaN, due to dissimilar number of "R-R" recordings due to artifacts
    d0 = d0.dropna() # Drop empty rows
    # Compute new cRR without NaN (empty rows and colums)
    cRR = np.cumsum(d0["Artifact corrected RR"])
    s0 = starts[i]
    # Create a list of time stamps for each data point
    Time = [pd.Timestamp(s0) + pd.Timedelta(seconds=i/1000) for i in cRR] 
    d0["Time"] = Time # Add the time stamp column to the data frame
    # Calculate Heart Rate pr. min (bpm) from the R-R intervals
    bpm = 60/(d0["Artifact corrected RR"]/1000)
    d0["Heart Rate"] = bpm # Add column of HR (beats per minute) to the data frame
    dphy[i] = d0
    


    
### ------------------------------------------------------------------------------------ ###
### Update "virtual" data frame with time stamps and beats per minute

dvir = data_frames_virtual
starts = start_times_virtual
for i in range(len(dvir)):
    d0 = dvir[i]
    d0 = d0.drop("Unnamed: 3", axis=1) # Drop empty column
    # Ensure the corrected and non-corrected accounts for all data
    RR = np.cumsum(d0["RR"])
    cRR = np.cumsum(d0["Artifact corrected RR"])
    if np.nanmax(RR) != np.nanmax(cRR):
        print("The cumulative times are not the same for corrected and uncorrected")
        print(f"For subject {i}, there is a difference of {np.nanmax(RR)-np.nanmax(cRR)}")
    # Drop rows with NaN, due to dissimilar number of "R-R" recordings due to artifacts
    d0 = d0.dropna() # Drop empty rows
    # Compute new cRR without NaN (empty rows and colums)
    cRR = np.cumsum(d0["Artifact corrected RR"])
    s0 = starts[i]
    # Create a list of time stamps for each data point
    Time = [pd.Timestamp(s0) + pd.Timedelta(seconds=i/1000) for i in cRR] 
    d0["Time"] = Time # Add the time stamp column to the data frame
    # Calculate Heart Rate pr. min (bpm) from the R-R intervals
    bpm = 60/(d0["Artifact corrected RR"]/1000)
    d0["Heart Rate"] = bpm # Add column of HR (beats per minute) to the data frame
    dvir[i] = d0

### ------------------------------------------------------------------------------------ ###
### Cutting the signals to only contain the lecture

# Define lecture start and end time 
phy_lecture_start_time = datetime.datetime.strptime("21.03.2023 11:10:00", "%d.%m.%Y %H:%M:%S")
phy_lecture_end_time = datetime.datetime.strptime("21.03.2023 13:10:11", "%d.%m.%Y %H:%M:%S")

# Loop through each data frame and select the rows with time stamps between the lecture start and end time
for i in range(len(dphy)):
    df = dphy[i]
    mask = (df["Time"] >= phy_lecture_start_time) & (df["Time"] <= phy_lecture_end_time)
    df = df.loc[mask]
    dphy[i] = df
    
for i in range(len(data_frames_virtual)):
    df = data_frames_virtual[i]
    mask = (df["Time"] >= phy_lecture_start_time) & (df["Time"] <= phy_lecture_end_time)
    df = df.loc[mask]
    data_frames_virtual[i] = df
    

### ------------------------------------------------------------------------------------ ###
### Plots

# Instantaneus heart rate (BPM) of a random student (only first 50 data points)
fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy[12].iloc[:51], x="Time", y="Heart Rate", color="blue")
sns.scatterplot(data=dphy[12].iloc[:51], x="Time", y="Heart Rate", color = "red",
                alpha=0.5)
plt.title("BPM based on corrected RR (data points 100-120)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()


# RR before and after Artifact detection (a random student)
fig, ax = plt.subplots(1,1)
sns.lineplot(data = dphy[12].iloc[10:], x="Time", y="RR", color = "red", label="Raw RR-data")
sns.lineplot(data = dphy[12].iloc[10:], x="Time", y="Artifact corrected RR", color = "blue", label="Cleaned RR-data")
plt.title("Artifact detection on RR")
plt.legend()
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()


# Normalize all signals (BPM only)
for i in range(len(dphy)):
    df = dphy[i]
    norm_data = (df["Heart Rate"]-np.mean(df["Heart Rate"]))/np.std(df["Heart Rate"])
    df["Normalized BPM"] = norm_data 
    dphy[i] = df
    
# Define break start and end time 
phy_break_start_time = datetime.datetime.strptime("21.03.2023 12:11:47", "%d.%m.%Y %H:%M:%S")
phy_break_end_time = datetime.datetime.strptime("21.03.2023 12:27:02", "%d.%m.%Y %H:%M:%S")

    
# Plot all normalized signals on top of eachother 
fig, ax = plt.subplots(1,1)
for i in range(len(start_times_physical)):
    sns.lineplot(data = dphy[i], x="Time", y="Normalized BPM", color = "blue")
# add a shaded rectangle to indicate the lecture break interval
ax.axvspan(phy_break_start_time, phy_break_end_time, color='grey', alpha=0.2)
plt.title("All normalized BPM")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.text(0.53, 0.9, "Break", color="black", transform=ax.transAxes) 
plt.show()



# ------------------------------------------------------------------------------------
## Li's plots ##

# Plot with the actual times
fig, ax = plt.subplots(1,1)
sns.lineplot(data = dphy[1], x="Time", y="Artifact corrected RR", color = "red")
sns.lineplot(data = dphy[2], x="Time", y="Artifact corrected RR", color = "blue")
plt.title("Artifact Corrected RR")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()

# With the actual dots
fig, ax = plt.subplots(1,1)
sns.scatterplot(data = dphy[0], x="Time", y="Artifact corrected RR", color = "red",
                alpha=0.5)
sns.scatterplot(data = dphy[1], x="Time", y="Artifact corrected RR", color = "blue",
                alpha=0.5)
plt.title("Artifact Corrected RR")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()

# Non-corrected raw data
fig, ax = plt.subplots(1,1)
sns.lineplot(data = dphy[0], x="Time", y="RR", color = "red")
sns.lineplot(data = dphy[1], x="Time", y="RR", color = "blue")
plt.title("Raw RR")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()

# Instantaneus heart rate (BPM)
fig, ax = plt.subplots(1,1)
sns.lineplot(data = dphy[0], x="Time", y="Heart Rate", color = "red")
sns.lineplot(data = dphy[1], x="Time", y="Heart Rate", color = "blue")
plt.title("BPM based on corrected RR")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()


### ------------------------------------------------------------------------------------ ###
### Li's code ###
# They are misaligned
# Interpolation and resampling at common time points
# Convert times to float timestamps
Ch_timestamps = [pd.Timestamp(ele).timestamp() for ele in dphy[0]["Time"]]
Tch_timestamps = [pd.Timestamp(ele).timestamp() for ele in dphy[1]["Time"]]

# Round to nearest second and get the common timepoints between the two timeseries
common_timestamps = np.intersect1d(np.round(Ch_timestamps,0),np.round(Tch_timestamps,0))
# Remove the first and last timepoint in case of rounding up or down
common_timestamps = common_timestamps[1:-1]
# Upsample to sfreq of interest
sfreq = 10
max_diff = int(common_timestamps[-1]-common_timestamps[0])
upsampled_timestamps = np.linspace(common_timestamps[0],common_timestamps[-1],(sfreq*max_diff)+1)
### Li's code end ###


# Instead of finding common timestamp, use manual starting point (lecture start) and lecture end
# Check each subject/file for common timestamps to ensure the data is avaiable the entire lecture
# Loop through all files and interpolate
# THEN cut up the files into smaller bits for

for i in range(len(dphy)-1):
    d0_timestamps = dphy[i]
    d1_timestamps = dphy[i+1]
    # Convert times to float timestamps
    d0_timestamps = [pd.Timestamp(ele).timestamp() for ele in dphy[i]["Time"]]
    d1_timestamps = [pd.Timestamp(ele).timestamp() for ele in dphy[i+1]["Time"]]
    # Round to nearest second and get the common timepoints between the two timeseries
    common_timestamps = np.intersect1d(np.round(d0_timestamps,0),np.round(d1_timestamps,0))
    # Remove the first and last timepoint in case of rounding up or down
    common_timestamps = common_timestamps[1:-1]
    # Upsample to sfreq of interest
    sfreq = 10
    max_diff = int(common_timestamps[-1]-common_timestamps[0])
    upsampled_timestamps = np.linspace(common_timestamps[0],common_timestamps[-1],(sfreq*max_diff)+1)
    # Take into account Daylight Saving time and the timezone from UTC
    upsampled_datetimes = [datetime.datetime.fromtimestamp(ele-60*60) for ele in upsampled_timestamps]
    # Fit function for linear interpolation
    d0f = scipy.interpolate.interp1d(d0_timestamps,dphy[0]["Artifact corrected RR"], kind="linear")
    d1f = scipy.interpolate.interp1d(d1_timestamps,dphy[1]["Artifact corrected RR"], kind="linear")
    # Interpolate to common timestamps
    d0_interp = d0f(upsampled_timestamps)
    d1_interp = d1f(upsampled_timestamps)

    dphy[i] = d0_timestamps
    dphy[i+1] = d1_timestamps


# Take into account Daylight Saving time and the timezone from UTC
upsampled_datetimes = [datetime.datetime.fromtimestamp(ele-60*60) for ele in upsampled_timestamps]

# Fit function for linear interpolation
Chf = scipy.interpolate.interp1d(Ch_timestamps,dphy[0]["Artifact corrected RR"], kind="linear")
Tchf = scipy.interpolate.interp1d(Tch_timestamps,dphy[1]["Artifact corrected RR"], kind="linear")
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
plt.show()

# With dots
fig, ax = plt.subplots(1,1)
sns.scatterplot(data = resampled_df, x="Time", y="Chelina_cRR", color = "red")
sns.scatterplot(data = resampled_df, x="Time", y="Tch_cRR", color = "blue")
plt.title("Resampled aligned Artifact Corrected RR")
plt.show()




### Cross-correlation with scipy
norm_Ch_interp = (Ch_interp-np.mean(Ch_interp))/np.std(Ch_interp)
norm_Tch_interp = (Tch_interp-np.mean(Tch_interp))/np.std(Tch_interp)

cross_corr = scipy.signal.correlate(norm_Ch_interp, norm_Tch_interp, mode="full")
cross_corr /= len(cross_corr)
delays = np.linspace(-(len(Ch_interp)-1),len(Ch_interp)-1,len(cross_corr))
fig, ax = plt.subplots(1,1)
plt.plot(delays, cross_corr)

print(delays[np.argmax(cross_corr)])
