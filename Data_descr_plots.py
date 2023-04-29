from Resamling import pd, sns, plt, dphy, dvir, datetime, np, start_times_physical, start_times_virtual, mdates, dphy_resampled, dvir_resampled

### ------------------------------------------------------------------------------------ ###
### Plots

# Instantaneus heart rate (BPM) of a random physical student (only first 15 data points)
fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy[12].iloc[1:16], x="Time", y="Heart Rate", color="royalblue", label = "Heart rate signal")
sns.scatterplot(data=dphy_resampled[12].iloc[17:170], x="Time", y="Heart Rate", color = "crimson",
                alpha=0.5, label = "Resampled data points")
sns.scatterplot(data=dphy[12].iloc[1:16], x="Time", y="Heart Rate", color = "royalblue",
                alpha=0.5, label = "Original data points")
plt.title("BPM based on corrected RR (example snippet)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.legend()
plt.show()


# RR before and after Artifact detection (same random student)
fig, ax = plt.subplots(1,1)
sns.lineplot(data = dphy[12].iloc[10:], x="Time", y="RR", color = "crimson", label="Raw RR-data")
sns.lineplot(data = dphy[12].iloc[10:], x="Time", y="Artifact corrected RR", color = "royalblue", label="Cleaned RR-data")
plt.title("Artifact detection on RR")
plt.legend()
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()


# Normalize all signals (BPM only)
for i in range(len(dphy)): # Physical lecture
    df = dphy[i]
    norm_data = (df["Heart Rate"]-np.mean(df["Heart Rate"]))/np.std(df["Heart Rate"])
    df["Normalized BPM"] = norm_data 
    dphy[i] = df
for i in range(len(dvir)): # Virtual lecture
    df = dvir[i]
    norm_data = (df["Heart Rate"]-np.mean(df["Heart Rate"]))/np.std(df["Heart Rate"])
    df["Normalized BPM"] = norm_data 
    dvir[i] = df

# Define break start and end time 
phy_break_start_time = datetime.datetime.strptime("21.03.2023 14:11:47", "%d.%m.%Y %H:%M:%S")
phy_break_end_time = datetime.datetime.strptime("21.03.2023 14:27:02", "%d.%m.%Y %H:%M:%S")
vir_break_start_time = datetime.datetime.strptime("28.03.2023 13:55:42", "%d.%m.%Y %H:%M:%S")
vir_break_end_time = datetime.datetime.strptime("28.03.2023 14:14:40", "%d.%m.%Y %H:%M:%S")
    
# Plot all normalized signals on top of eachother 
# Physical
fig, ax = plt.subplots(1,1) 
for i in range(len(start_times_physical)):
    sns.lineplot(data = dphy[i], x="Time", y="Normalized BPM", color = "royalblue")
# add a shaded rectangle to indicate the lecture break interval
ax.axvspan(phy_break_start_time, phy_break_end_time, color='grey', alpha=0.2)
plt.title("All normalized BPM (Physical)")
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.text(0.53, 0.9, "Break", color="black", transform=ax.transAxes) 
plt.show() 

# Virtual
fig, ax = plt.subplots(1,1) 
for i in range(len(start_times_virtual)):
    sns.lineplot(data = dvir[i], x="Time", y="Normalized BPM", color = "royalblue")
# add a shaded rectangle to indicate the lecture break interval
ax.axvspan(vir_break_start_time, vir_break_end_time, color='grey', alpha=0.2)
plt.title("All normalized BPM (Virtual)")
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.text(0.41, 0.9, "Break", color="black", transform=ax.transAxes) 
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