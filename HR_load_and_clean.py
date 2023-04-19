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
    
