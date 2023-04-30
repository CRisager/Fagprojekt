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
### Load Data ###

# Loading the data files
# Physical
#path1 = "C:/Users/cheli/OneDrive/Skrivebord/Fagprojekt/Fagprojekt_data/physical"
path1 = "/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data/physical"
#path1 = "/Users/jesperberglund/Downloads/HR_Data/physical"
os.chdir(path1)
# Using list comprehension to loop over all files in folder minus the teacher
csv_files_physical = [f for f in os.listdir(path1) if f.endswith('.csv')][:-1]
# Sort the files from smallest to largest device number
csv_files_physical = sorted(csv_files_physical, key=lambda x: int(x.split('.')[0]))
# Read the teacher file independently
Teacher_phy = os.listdir(path1)[-1]
# Add the teacher to the end of the list
csv_files_physical = csv_files_physical + [Teacher_phy]

# Virtual
#path2 = "C:/Users/cheli/OneDrive/Skrivebord/Fagprojekt/Fagprojekt_data/virtual"
path2 = "/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data/virtual"
#path2 = "/Users/jesperberglund/Downloads/HR_Data/virtual"
os.chdir(path2)
# Using list comprehension to loop over all files in folder minus the teacher
csv_files_virtual = [f for f in os.listdir(path2) if f.endswith('.csv')][:-1]
# Sort the files from smallest to largest device number
csv_files_virtual = sorted(csv_files_virtual, key=lambda x: int(x.split('.')[0]))
# Read the teacher file independently
Teacher_vir = os.listdir(path2)[-1]
# Add the teacher to the end of the list
csv_files_virtual = csv_files_virtual + [Teacher_vir]


# Create lists for dataframes and starting times
data_frames_physical = []
data_frames_virtual = []
start_times_physical = []
start_times_virtual = []

# Function for loading data into dataframes and starting times
def Load_data(csv_files, data_frames, start_times, path):
    for file in csv_files:
        file_path = os.path.join(path, file)
        # Read the data as a pandas dataframe
        df = pd.read_csv(file_path, skiprows=2, sep=";")
        data_frames.append(df) # Add dataframe to list of dataframes
        # Read the starting time stamps from all readings
        start_time = pd.read_csv(file_path, skiprows=1, nrows=0, sep=";").columns[0].split(": ")[1]
        start_time = datetime.datetime.strptime(start_time, "%d.%m.%Y %H:%M:%S")
        start_times.append(start_time) # add to the start times list

print("...")

Load_data(csv_files_physical, data_frames_physical, start_times_physical, path1)
Load_data(csv_files_virtual, data_frames_virtual, start_times_virtual, path2)

print("Loading done \n ...")
    
### ------------------------------------------------------------------------------------ ###
### Update dataframes with time stamps and heart rate (beats per minute)

# Shorten the names to make it easier to work with
dphy = data_frames_physical 
starts_phy = start_times_physical
dvir = data_frames_virtual
starts_vir = start_times_virtual

# Function for updating the dataframes
def Update_df(df_list, starts_list):
    for i in range(len(df_list)):
        df = df_list[i]
        df = df.drop("Unnamed: 3", axis=1) # Drop empty column
        # Ensure the non-corrected and corrected RR accounts for all data
        RR = np.cumsum(df["RR"])
        cRR = np.cumsum(df["Artifact corrected RR"])
        
        #if np.nanmax(RR) != np.nanmax(cRR):
        #    print("The cumulative times are not the same for corrected and uncorrected")
        #    print(f"For subject {i}, there is a difference of {np.nanmax(RR)-np.nanmax(cRR)}")
        
        # Drop rows with NaN, due to dissimilar number of "R-R" recordings due to artifacts
        df = df.dropna() # Drop empty rows
        # Compute new cRR without NaN (empty rows and colums)
        cRR = np.cumsum(df["Artifact corrected RR"])
        s0 = starts_list[i]
        # Create a list of time stamps for each data point
        Time = [pd.Timestamp(s0) + pd.Timedelta(seconds=i/1000) for i in cRR] 
        
        # Change time stamps to danish timezone
        if df_list == dphy:
            Time = [t + pd.Timedelta(hours=2) for t in Time]
        elif df_list == dvir:
            Time = [t + pd.Timedelta(hours=3) for t in Time] # Take summer-time into account
        else:
            print("What timezone are you dealing with here??")

        df["Time"] = Time # Add the time stamp column to the data frame
        # Calculate Heart Rate pr. min (bpm) from the R-R intervals
        bpm = 60/(df["Artifact corrected RR"]/1000)
        df["Heart Rate"] = bpm # Add column of HR (beats per minute) to the data frame
        df_list[i] = df

Update_df(dphy, starts_phy)
Update_df(dvir, starts_vir)

print("Dataframe updates done")


### ------------------------------------------------------------------------------------ ###
### Cutting the signals to only contain the lecture (+ a little padding for resampling)

# Define lecture start and end time (+ a padding on 1 minute) in UTC timezone
phy_lecture_start_plus = datetime.datetime.strptime("21.03.2023 13:09:00", "%d.%m.%Y %H:%M:%S")
phy_lecture_end_plus = datetime.datetime.strptime("21.03.2023 15:11:11", "%d.%m.%Y %H:%M:%S")
vir_lecture_start_plus = datetime.datetime.strptime("28.03.2023 13:20:25", "%d.%m.%Y %H:%M:%S")
vir_lecture_end_plus = datetime.datetime.strptime("28.03.2023 15:14:37", "%d.%m.%Y %H:%M:%S")

# Function for cutting the data 
def Cutting(start, end, df_list):    
    # Loop through each data frame and select the rows with time stamps between the lecture start and end time
    for i in range(len(df_list)): 
        df = df_list[i]
        mask = (df["Time"] >= start) & (df["Time"] <= end)
        df = df.loc[mask]
        # Round the first time stamp down to the nearest second aka the lecture start
        #df.iloc[0, df.columns.get_loc('Time')] = pd.to_datetime('2023-03-21 11:10:00.00000').floor('s')
        df_list[i] = df

Cutting(phy_lecture_start_plus, phy_lecture_end_plus, dphy) # Physical lecture
Cutting(vir_lecture_start_plus, vir_lecture_end_plus, dvir) # Virtual lecture

print("Cutting signal done")