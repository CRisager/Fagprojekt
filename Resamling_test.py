from HR_load_and_clean import sns, scipy, plt, dphy, dvir, datetime, np, pd


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


# Reampling the signals from the physical lecture
print("Resampling of physical lecture")
for i in range(len(dphy)):
    df = dphy[i]
    
    # Keep track of which dataframe is reached
    print(i, "/", len(dphy))

    # Convert time stamps to float
    timestamps = [pd.Timestamp(ele).timestamp() for ele in df["Time"]]
    lecture_start = pd.Timestamp(phy_lecture_start_time).timestamp()
    lecture_end = pd.Timestamp(phy_lecture_end_time).timestamp()

    # Determine the new sampling frequency
    freq_new = 10 # Hz
    # Determine the length of the lecture
    lecture_length = int(lecture_end - lecture_start)
    # Create a list of the upsampled time stamps
    upsampled_timestamps = np.linspace(lecture_start,lecture_end,(freq_new*lecture_length)+1)

    # Fit a linear interpolation function to the existing time stamps and RR-values
    f = scipy.interpolate.interp1d(timestamps,df["Artifact corrected RR"], kind="linear")
    # Interpolate the signals
    RR_resampled = f(upsampled_timestamps) 

    # Convert time stamps back to pandas datetime objects
    timestamps_resampled = [pd.Timestamp.fromtimestamp(ele) for ele in upsampled_timestamps]


    for i in range(len(dphy)):
        # create a new DataFrame with a unique name based on the loop index
        df_name = 'df{}_resampled'.format(0)
        df = pd.DataFrame({'RR_resampled': RR_resampled, 'Time_resampled': timestamps_resampled})

        # assign the new DataFrame to a variable with the unique name
        globals()[df_name] = df
        dphy_resampled.append(globals()[df_name])        
        
        
# Reampling the signals from the virtual lecture
print("Resampling of physical lecture")
for i in range(len(dvir)):
    df = dvir[i]
    
    # Keep track of which dataframe is reached
    print(i, "/", len(dvir))

    # Convert time stamps to float
    timestamps = [pd.Timestamp(ele).timestamp() for ele in df["Time"]]
    lecture_start = pd.Timestamp(vir_lecture_start_time).timestamp()
    lecture_end = pd.Timestamp(vir_lecture_end_time).timestamp()

    # Determine the new sampling frequency
    freq_new = 10 # Hz
    # Determine the length of the lecture
    lecture_length = int(lecture_end - lecture_start)
    # Create a list of the upsampled time stamps
    upsampled_timestamps = np.linspace(lecture_start,lecture_end,(freq_new*lecture_length)+1)

    # Fit a linear interpolation function to the existing time stamps and RR-values
    f = scipy.interpolate.interp1d(timestamps,df["Artifact corrected RR"], kind="linear")
    # Interpolate the signals
    RR_resampled = f(upsampled_timestamps) 

    # Convert time stamps back to pandas datetime objects
    timestamps_resampled = [pd.Timestamp.fromtimestamp(ele) for ele in upsampled_timestamps]


    for i in range(len(dvir)):
        # create a new DataFrame with a unique name based on the loop index
        df_name = 'df{}_resampled'.format(0)
        df = pd.DataFrame({'RR_resampled': RR_resampled, 'Time_resampled': timestamps_resampled})

        # assign the new DataFrame to a variable with the unique name
        globals()[df_name] = df
        dvir_resampled.append(globals()[df_name])
