from Resamling import pd, sns, plt, dphy, dvir, datetime, np, start_times_physical, start_times_virtual, mdates, dphy_resampled, dvir_resampled

### ------------------------------------------------------------------------------------ ###
### Plots

# Instantaneus heart rate (BPM) of a random physical student (only first 15 data points)
fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy_resampled[12].iloc[16:170], x="Time", y="Heart Rate", color="royalblue", label = "Resampled heart rate signal")
sns.scatterplot(data=dphy[12].iloc[1:16], x="Time", y="Heart Rate", color = "crimson",
                alpha=0.5, label = "Original data points")
plt.title("BPM based on corrected RR (example snippet)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
handles, labels = plt.gca().get_legend_handles_labels() # Get handles and labels for costomized legend()
order = [1,0] # Specify order of items in legend
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order]) # Add legend to plot
plt.show()


# BPM original vs resampled (same student and data points)
fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy[12].iloc[1:16], x="Time", y="Heart Rate", color="royalblue", label = "Original heart rate signal")
sns.lineplot(data=dphy_resampled[12].iloc[17:170], x="Time", y="Heart Rate", color="crimson", label = "Resampled heart rate signal")
sns.scatterplot(data=dphy_resampled[12].iloc[17:170], x="Time", y="Heart Rate", color = "crimson",
                alpha=0.5, label = "Resampled data points")
sns.scatterplot(data=dphy[12].iloc[1:16], x="Time", y="Heart Rate", color = "royalblue",
                alpha=0.75, label = "Original data points")
plt.title("BPM based on corrected RR (example snippet)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
handles, labels = plt.gca().get_legend_handles_labels() # Get handles and labels for costomized legend()
order = [0,1,3,2] # Specify order of items in legend
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order]) # Add legend to plot
plt.show()


# RR before and after Artifact detection (same random student)
fig, ax = plt.subplots(1,1)
sns.lineplot(data = dphy[12].iloc[10:], x="Time", y="RR", color = "crimson", label="Raw RR-data")
sns.lineplot(data = dphy[12].iloc[10:], x="Time", y="Artifact corrected RR", color = "royalblue", label="Cleaned RR-data")
plt.title("Artifact detection on RR")
plt.legend()
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()



# Normalize all resampled signals (BPM only)
for i in range(len(dphy_resampled)): # Physical lecture
    df = dphy_resampled[i]
    norm_data = (df["Heart Rate"]-np.mean(df["Heart Rate"]))/np.std(df["Heart Rate"])
    df["Normalized BPM"] = norm_data 
    dphy_resampled[i] = df
for i in range(len(dvir_resampled)): # Virtual lecture
    df = dvir_resampled[i]
    norm_data = (df["Heart Rate"]-np.mean(df["Heart Rate"]))/np.std(df["Heart Rate"])
    df["Normalized BPM"] = norm_data 
    dvir_resampled[i] = df

# Define break start and end time 
phy_break_start_time = datetime.datetime.strptime("21.03.2023 14:11:47", "%d.%m.%Y %H:%M:%S")
phy_break_end_time = datetime.datetime.strptime("21.03.2023 14:27:02", "%d.%m.%Y %H:%M:%S")
vir_break_start_time = datetime.datetime.strptime("28.03.2023 13:55:42", "%d.%m.%Y %H:%M:%S")
vir_break_end_time = datetime.datetime.strptime("28.03.2023 14:14:40", "%d.%m.%Y %H:%M:%S")
    
# Plot all normalized signals on top of eachother 
# Physical
fig, ax = plt.subplots(1,1) 
for i in range(len(start_times_physical)):
    sns.lineplot(data = dphy_resampled[i], x="Time", y="Normalized BPM", color = "royalblue")
# Add a shaded rectangle to indicate the lecture break interval
ax.axvspan(phy_break_start_time, phy_break_end_time, color='grey', alpha=0.2)
plt.text(0.53, 0.9, "Break", color="black", transform=ax.transAxes) 
# Format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.title("All normalized BPM (Physical)") 
plt.show() 

# Virtual
fig, ax = plt.subplots(1,1) 
for i in range(len(start_times_virtual)):
    sns.lineplot(data = dvir_resampled[i], x="Time", y="Normalized BPM", color = "royalblue")
# add a shaded rectangle to indicate the lecture break interval
ax.axvspan(vir_break_start_time, vir_break_end_time, color='grey', alpha=0.2)
plt.title("All normalized BPM (Virtual)")
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.text(0.325, 0.9, "Break", color="black", transform=ax.transAxes) 
plt.show()
