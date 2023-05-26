from Resampling import pd, sns, plt, dphy, dvir, datetime, np, start_times_physical, start_times_virtual, mdates, dphy_resampled, dvir_resampled

### ------------------------------------------------------------------------------------ ###
### Plots

"""
# Instantaneus heart rate (BPM) of a random physical student (only 15 data points)
fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy_resampled[12].iloc[81:196], x="Time", y="Heart Rate", color="royalblue", label = "Resampled heart rate signal")
sns.scatterplot(data=dphy[12].iloc[10:26], x="Time", y="Heart Rate", color = "crimson",
                alpha=0.5, label = "Original data points")
plt.title("BPM based on corrected RR (example snippet)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
handles, labels = plt.gca().get_legend_handles_labels() # Get handles and labels for costomized legend()
order = [1,0] # Specify order of items in legend
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order]) # Add legend to plot
plt.show()
"""

# BPM original vs resampled (same student and data points)
fig, ax = plt.subplots(1, 1)
sns.lineplot(data=dphy[12].iloc[10:26], x="Time", y="Heart Rate", color="royalblue", label = "Original heart rate signal")
sns.lineplot(data=dphy_resampled[12].iloc[81:196], x="Time", y="Heart Rate", color="crimson", label = "Resampled heart rate signal")
sns.scatterplot(data=dphy_resampled[12].iloc[81:196], x="Time", y="Heart Rate", color = "crimson",
                alpha=0.5, label = "Resampled data points")
sns.scatterplot(data=dphy[12].iloc[10:26], x="Time", y="Heart Rate", color = "royalblue",
                alpha=0.75, label = "Original data points")
plt.title("BPM based on corrected RR (example snippet)")
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
handles, labels = plt.gca().get_legend_handles_labels() # Get handles and labels for costomized legend()
order = [0,1,3,2] # Specify order of items in legend
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order]) # Add legend to plot
plt.show()


# RR before and after Artifact detection (new random student)
fig, ax = plt.subplots(1,1)
sns.lineplot(data = dphy[10].iloc[10:], x="Time", y="RR", color = "crimson", label="Raw RR-data")
sns.lineplot(data = dphy[10].iloc[10:], x="Time", y="Artifact corrected RR", color = "royalblue", label="Cleaned RR-data")
plt.title("Artifact detection on RR")
plt.legend()
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()


####### Average heart rate (BPM) ######################################################################
# Create an empty list for the average signal
phy_average_signal = []
vir_average_signal = []

# Create a matrix of the data to be used
phy_BPM_matrix = []
vir_BPM_matrix = []

for i in range(len(dphy_resampled)): # Physical lecture
    df = dphy_resampled[i]
    phy_BPM_matrix.append(list(df["Heart Rate"]))
for i in range(len(dvir_resampled)): # Virtual lecture
    df = dvir_resampled[i]
    vir_BPM_matrix.append(list(df["Heart Rate"]))

# Loop over all the signals and get the average values
for elements in zip(*phy_BPM_matrix): # Physical lecture
    average = sum(elements) / len(elements)
    phy_average_signal.append(average)
for elements in zip(*vir_BPM_matrix): # Virtual lecture
    average = sum(elements) / len(elements)
    vir_average_signal.append(average)

# Create datafraes for the new data 
phy_dataframe = pd.DataFrame({'Time': dphy_resampled[0]["Time"], 'Heart Rate': phy_average_signal})
vir_dataframe = pd.DataFrame({'Time': dvir_resampled[0]["Time"], 'Heart Rate': vir_average_signal})

# Define break start and end time 
phy_break_start_time = datetime.datetime.strptime("21.03.2023 14:11:47", "%d.%m.%Y %H:%M:%S")
phy_break_end_time = datetime.datetime.strptime("21.03.2023 14:27:02", "%d.%m.%Y %H:%M:%S")
vir_break_start_time = datetime.datetime.strptime("28.03.2023 13:55:42", "%d.%m.%Y %H:%M:%S")
vir_break_end_time = datetime.datetime.strptime("28.03.2023 14:14:40", "%d.%m.%Y %H:%M:%S")

# Plot the average signal
# Physical
fig, ax = plt.subplots(1,1) 
sns.lineplot(data = phy_dataframe, x="Time", y="Heart Rate (BPM)", color = "royalblue", label="Average signal")
# Add a shaded rectangle to indicate the lecture break interval
ax.axvspan(phy_break_start_time, phy_break_end_time, color='grey', alpha=0.2)
plt.text(0.53, 0.9, "Break", color="black", transform=ax.transAxes) 
# Format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.title("Average BPM for physical lecture") 
plt.show() 

# Virtual
fig, ax = plt.subplots(1,1) 
sns.lineplot(data = vir_dataframe, x="Time", y="Heart Rate (BPM)", color = "royalblue", label="Average signal")
# Add a shaded rectangle to indicate the lecture break interval
ax.axvspan(vir_break_start_time, vir_break_end_time, color='grey', alpha=0.2)
plt.text(0.32, 0.9, "Break", color="black", transform=ax.transAxes) 
# Format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.title("Average BPM for virtual lecture") 
plt.show() 