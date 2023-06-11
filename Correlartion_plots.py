from Correlation_calculation import (sns, plt, np, mdates, dphy_resampled, dvir_resampled, phy_sections,
                           vir_sections, df_list_quiz_phy, df_list_quiz_vir, scipy)


############## Plot: Correlation as a functions of delay/shift ################################

# Teacher/student correlation (entire signal)
Student = dphy_resampled[0]["RR"]
Teacher = dphy_resampled[-1]["RR"]

signal1_norm = (Student-np.mean(Student))/np.std(Student)
signal2_norm = (Teacher-np.mean(Teacher))/np.std(Teacher)
# Calculate cross-correlations
cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
cross_corr /= len(signal1_norm)
# Maximum shift is 1 minute
delays = np.linspace(-(len(Student)-1),len(Teacher)-1,len(cross_corr))
delays /= 10 # go from samples to seconds. 10 Hz = 10 samples in 1 second

fig, ax = plt.subplots(1,1)
plt.plot(delays, cross_corr)
plt.title("Correlation as a function of delay")
plt.xlabel("Delay in seconds")
plt.ylabel("Correlation")
plt.show()


# Teacher/student correlation (third section)
# Define signals 
signal1 = phy_sections[3][0]["RR"]
signal2 = phy_sections[3][-1]["RR"]
# Normalize 
signal1_norm = (signal1-np.mean(signal1))/np.std(signal1)
signal2_norm = (signal2-np.mean(signal2))/np.std(signal2)
# Calculate cross-correlations
cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
cross_corr /= len(signal1_norm)
# Maximum shift is 1 minute
delays = np.linspace(-(len(signal1)-1),len(signal2)-1,len(cross_corr))
delays = delays/10

fig, ax = plt.subplots(1,1)
plt.plot(delays, cross_corr)
plt.title("Correlation as a function of delay")
plt.xlabel("Delay in seconds")
plt.ylabel("Correlation")
plt.show()


# Teacher/student correlation (third section) with 1 minute 
# Define signals 
signal1 = vir_sections[3][0]["RR"]
signal2 = vir_sections[3][-1]["RR"]
# Normalize 
signal1_norm = (signal1-np.mean(signal1))/np.std(signal1)
signal2_norm = (signal2-np.mean(signal2))/np.std(signal2)
# Calculate cross-correlations
cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
cross_corr /= len(signal1_norm)
# Maximum shift is 1 minute
delays = np.linspace(-(len(signal1)-1),len(signal2)-1,len(cross_corr))
delays = delays/10
max_shift_corr = [cross_corr[i] for i in range(len(delays)) if delays[i] > -60 and delays[i] < 60]
max_shift_delays = [num for num in delays if num > -60 and num < 60]

fig, ax = plt.subplots(1,1)
plt.plot(max_shift_delays, max_shift_corr)
plt.title("Correlation as a function of delay (1 min)")
plt.xlabel("Delay in seconds")
plt.ylabel("Correlation")
plt.show()


# Teacher/student correlation (third section) with 1 second 
# Define signals 
signal1 = phy_sections[3][0]["RR"]
signal2 = phy_sections[3][-1]["RR"]
# Normalize 
signal1_norm = (signal1-np.mean(signal1))/np.std(signal1)
signal2_norm = (signal2-np.mean(signal2))/np.std(signal2)
# Calculate cross-correlations
cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
cross_corr /= len(signal1_norm)
# Maximum shift is 1 minute
delays = np.linspace(-(len(signal1)-1),len(signal2)-1,len(cross_corr))
delays = delays/10
max_shift_corr = [cross_corr[i] for i in range(len(delays)) if delays[i] >= -1 and delays[i] <= 1]
max_shift_delays = [num for num in delays if num >= -1 and num <= 1]
plot_delays = [int(num*1000) for num in max_shift_delays]

fig, ax = plt.subplots(1,1)
plt.scatter(plot_delays, max_shift_corr)
plt.title("Correlation as a function of delay (1 sec)")
plt.xlabel("Delay in miliseconds")
plt.ylabel("Correlation")
plt.show()


############## Plot: High vs low correlation ################################

# Determine the index of the highest and lowest correlations
max_corr_index = df_list_quiz_phy[0]["Teacher/Student corr"].idxmax()
min_corr_index = df_list_quiz_phy[0]["Teacher/Student corr"].idxmin()

# Define teacher and max/min correlation students
teacher = phy_sections[0][-1]
min_corr_student = phy_sections[0][min_corr_index]
max_corr_student = phy_sections[0][max_corr_index]
# Normalize RR-values
teacher["RR"] = (teacher["RR"]-np.mean(teacher["RR"]))/np.std(teacher["RR"])
min_corr_student["RR"] = (min_corr_student["RR"]-np.mean(min_corr_student["RR"]))/np.std(min_corr_student["RR"])
max_corr_student["RR"] = (max_corr_student["RR"]-np.mean(max_corr_student["RR"]))/np.std(max_corr_student["RR"])

# Plot of a student with the lowest correlation with teacher
fig, ax = plt.subplots(1,1)
sns.lineplot(data = min_corr_student, x="Time", y="RR", color = "crimson", label="student")
sns.lineplot(data = teacher, x="Time", y="RR", color = "green", label="teacher")
plt.title("Low correlation")
plt.legend()
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()

# Plot of a student with the highest correlation with teacher
fig, ax = plt.subplots(1,1)
sns.lineplot(data = max_corr_student, x="Time", y="RR", color = "crimson", label="student")
sns.lineplot(data = teacher, x="Time", y="RR", color = "green", label="teacher")
plt.title("High correlation")
plt.legend()
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()
