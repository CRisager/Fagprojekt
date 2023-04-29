from HR_load_and_clean import sns, scipy, plt, dphy, dvir, datetime, np, pd, Cutting, start_times_physical, start_times_virtual, mdates


# Define lecture start and end time 
phy_lecture_start_time = datetime.datetime.strptime("21.03.2023 11:10:00", "%d.%m.%Y %H:%M:%S")
phy_lecture_end_time = datetime.datetime.strptime("21.03.2023 13:10:11", "%d.%m.%Y %H:%M:%S")
vir_lecture_start_time = datetime.datetime.strptime("28.03.2023 10:21:25", "%d.%m.%Y %H:%M:%S")
vir_lecture_end_time = datetime.datetime.strptime("28.03.2023 12:13:37", "%d.%m.%Y %H:%M:%S")


### ------------------------------------------------------------------------------------ ###
### Resampling to a higher frequency 

# Create a list for all the resampled dataframes
dphy_resampled = []
dvir_resampled = []

# Function for resampling
def Resamling(start, end, df_list):
    for i in range(len(df_list)):
        df = df_list[i]
        
        # Keep track of which dataframe is being resampled
        print(i, "/", len(df_list))

        # Convert time stamps to float
        timestamps = [pd.Timestamp(ele).timestamp() for ele in df["Time"]]
        lecture_start = pd.Timestamp(start).timestamp()
        lecture_end = pd.Timestamp(end).timestamp()

        # Determine the new sampling frequency
        freq_new = 10 # Hz
        # Determine the length of the lecture
        lecture_length = int(lecture_end - lecture_start)
        # Create a list of the upsampled time stamps
        upsampled_timestamps = np.linspace(lecture_start,lecture_end,(freq_new*lecture_length)+1)

        # Fit a linear interpolation function to the measured time stamps and RR-values
        f = scipy.interpolate.interp1d(timestamps,df["Artifact corrected RR"], kind="linear")
        # Interpolate the signal creating new RR-intervals based on the upsampled timestamps
        RR_resampled = f(upsampled_timestamps) 

        # Convert time stamps back to pandas datetime objects
        timestamps_resampled = [pd.Timestamp.fromtimestamp(ele) for ele in upsampled_timestamps]

        # Calculate new BPM based on the resampled RR-intervals
        BPM_resampled = 60/(RR_resampled/1000)

        # Create a new DataFrame with a unique name based on the loop index
        df_name = 'df{}_resampled'.format(0)
        df = pd.DataFrame({'RR': RR_resampled, 'Time': timestamps_resampled, 'Heart Rate': BPM_resampled})

        # assign the new DataFrame to a variable with the unique name
        globals()[df_name] = df
        if df_list == dphy:
            dphy_resampled.append(globals()[df_name]) 
        elif df_list == dvir:       
            dvir_resampled.append(globals()[df_name]) 
        else:
            print("What is df_list??")

# Resample         
Resamling(phy_lecture_start_time, phy_lecture_end_time, dphy) # Physical lecture
Resamling(vir_lecture_start_time, vir_lecture_end_time, dvir) # Virtual lecture

print("Re-sampling done")