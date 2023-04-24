from HR_load_and_clean import sns, plt, dphy, dvir, data_frames_virtual, datetime, np, pd

### ------------------------------------------------------------------------------------ ###
### Cutting the signals to only contain the lecture

# Define lecture start and end time 
phy_lecture_start_time = datetime.datetime.strptime("21.03.2023 11:10:00", "%d.%m.%Y %H:%M:%S")
phy_lecture_end_time = datetime.datetime.strptime("21.03.2023 13:10:11", "%d.%m.%Y %H:%M:%S")
vir_lecture_start_time = datetime.datetime.strptime("28.03.2023 10:21:25", "%d.%m.%Y %H:%M:%S")
vir_lecture_end_time = datetime.datetime.strptime("28.03.2023 12:13:37", "%d.%m.%Y %H:%M:%S")


# Loop through each data frame and select the rows with time stamps between the lecture start and end time
# Round the first time stamp down to the nearest second aka the lecture start
for i in range(len(dphy)): # Physical lecture
    df = dphy[i]
    mask = (df["Time"] >= phy_lecture_start_time) & (df["Time"] <= phy_lecture_end_time)
    df = df.loc[mask]
    df.iloc[0, df.columns.get_loc('Time')] = pd.to_datetime('2023-03-21 11:10:00.00000').floor('s')
    dphy[i] = df
    
for i in range(len(dvir)): # Virtual lecture
    df = dvir[i]
    mask = (df["Time"] >= vir_lecture_start_time) & (df["Time"] <= vir_lecture_end_time)
    df = df.loc[mask]
    df.iloc[0, df.columns.get_loc('Time')] = pd.to_datetime('2023-03-21 11:10:00.00000').floor('s')
    data_frames_virtual[i] = df


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

print(dphy[1]["Time"][1:5])






import pandas as pd

def resample_signal(df, sampling_rate):
    df['Time'] = pd.to_datetime(df['Time'], unit='s')
    df = df.set_index('Time')
    df_resampled = df.resample(str(int(1/sampling_rate*1000)) + 'ms').mean()
    df_resampled = df_resampled.reset_index()
    df_resampled.columns = ['Time_resampled', 'RR_resampled']
    return df_resampled


# Resample all signals to 10 Hz
dphy_resampled = [resample_signal(df, 10) for df in dphy]









print(dphy[1]["Time"][1:5])



fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy[0].iloc[:51], x="Time", y="Heart Rate", color="blue")
sns.scatterplot(data=dphy[0].iloc[:51], x="Time", y="Heart Rate", color = "red",
                alpha=0.5)
plt.title("BPM based on corrected RR (data points 100-120)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()

 

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