import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import datetime
import pytz
import matplotlib.dates as mdates


### ------------------------------------------------------------------------------------ ### 
### Working Directory for physical ###
path = "C:/Users/cheli/OneDrive/Skrivebord/Fagprojekt/Fagprojekt_data/physical"
# path = = "/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data/physical"
#path = "/Users/jesperberglund/Downloads/HR_Data/physical"
os.chdir(path)

# Using list comprehension to loop over all files in folder (minus the teacher and Chelina)
csv_files_physical = [f for f in os.listdir(path) if f.endswith('.csv')][:len(os.listdir(path))-2]

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
csv_files_virtual = [f for f in os.listdir(path) if f.endswith('.csv')][:len(os.listdir(path))-2]

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
### Resampling to a higher frequency 


# Instantaneus heart rate (BPM) of a random physical student (only first 50 data points)
fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy[0].iloc[:51], x="Time", y="Heart Rate", color="blue")
sns.scatterplot(data=dphy[0].iloc[:51], x="Time", y="Heart Rate", color = "red",
                alpha=0.5)
plt.title("BPM based on corrected RR (data points 100-120)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()

print(dphy[1]["Time"][1])


import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


def upsample_dataframe(df):
    # Calculate the time intervals between each RR interval
    time_intervals = df['Time'].diff().dt.total_seconds().values

    # Calculate the new time intervals for the upsampled signal. We want to upsample the signal to 10 Hz, so the new time intervals will be 0.1 seconds.
    new_time_intervals = np.arange(0, len(df)-1, 0.1)

    # Create a function to interpolate the signal. We will use linear interpolation for simplicity.
    f = interp1d(time_intervals, df['Artifact corrected RR'].iloc[:-1], kind='linear')

    # Interpolate the signal using the new time intervals.
    upsampled_rr_intervals = f(new_time_intervals)

    # Calculate the new BPM values
    upsampled_bpm = 60 / upsampled_rr_intervals

    # Create a new dataframe with the upsampled data
    upsampled_df = pd.DataFrame({'Time': pd.date_range(start=df['Time'].iloc[0], periods=len(upsampled_rr_intervals), freq='0.1S'),
                                 'Artifact corrected RR': upsampled_rr_intervals,
                                 'Heart Rate': upsampled_bpm})

    return upsampled_df

for i in range(len(dphy)):
    dphy[i]=upsample_dataframe(dphy[i])

    
    

# Instantaneus heart rate (BPM) of a random physical student (only first 50 data points)
fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy[0].iloc[:51], x="Time", y="Heart Rate", color="blue")
sns.scatterplot(data=dphy[0].iloc[:51], x="Time", y="Heart Rate", color = "red",
                alpha=0.5)
plt.title("BPM based on corrected RR (data points 100-120)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()

print(dphy[1]["Time"][1])
 

### ------------------------------------------------------------------------------------ ###
### Cutting the signals to only contain the lecture

# Define lecture start and end time 
phy_lecture_start_time = datetime.datetime.strptime("21.03.2023 11:10:00", "%d.%m.%Y %H:%M:%S")
phy_lecture_end_time = datetime.datetime.strptime("21.03.2023 13:10:11", "%d.%m.%Y %H:%M:%S")
vir_lecture_start_time = datetime.datetime.strptime("28.03.2023 10:21:25", "%d.%m.%Y %H:%M:%S")
vir_lecture_end_time = datetime.datetime.strptime("28.03.2023 12:13:37", "%d.%m.%Y %H:%M:%S")

# Loop through each data frame and select the rows with time stamps between the lecture start and end time
for i in range(len(dphy)): # Physical lecture
    df = dphy[i]
    mask = (df["Time"] >= phy_lecture_start_time) & (df["Time"] <= phy_lecture_end_time)
    df = df.loc[mask]
    dphy[i] = df
    
for i in range(len(dvir)): # Virtual lecture
    df = dvir[i]
    mask = (df["Time"] >= vir_lecture_start_time) & (df["Time"] <= vir_lecture_end_time)
    df = df.loc[mask]
    data_frames_virtual[i] = df
    
print(phy_lecture_end_time)