from Split_signals import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled,
                           dphy_students, dvir_students, phy_sections, vir_sections, df_quiz_phy, df_quiz_vir)
import scipy

############################################################## 
### Create the correct dataframes ###

# Add a state column to the dataframes for physical and virtual
state1 = ["Physical"] * len(df_quiz_phy)
df_quiz_phy["State"] = state1
state2 = ["Virtual"] * len(df_quiz_vir)
df_quiz_vir["State"] = state2
# Create a list of dataframes, one for each section
df_list_quiz_phy = [df_quiz_phy.copy() for _ in range(7)]
df_list_quiz_vir = [df_quiz_vir.copy() for _ in range(6)]



############################################################## 
### Cross-correlation ###
def MaxCorr(signal1, signal2, min_shift, max_shift):
    # Normalize signals
    signal1_norm = (signal1-np.mean(signal1))/np.std(signal1)
    signal2_norm = (signal2-np.mean(signal2))/np.std(signal2)
    # Calculate cross-correlations (Maximum shift is 1 minute)   
    cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
    cross_corr /= len(signal1_norm)
    delays = np.linspace(-(len(signal1_norm)-1),len(signal2_norm)-1,len(cross_corr)) # list of delays
    delays /= 10 # Go from samples to seconds. 10 Hz = 10 samples in 1 second
    # Create a list of correlations within the max shift of (1 sec or 1 min depending on phy/vir)
    max_shift_corr = [cross_corr[i] for i in range(len(delays)) if delays[i] >= min_shift and delays[i] <= max_shift]
    max_corr = max(max_shift_corr) # Find maximum correlation within this 
    return max_corr

def Correlations(total_list, df_quiz_list, i):
    # Define the teachers RR-intervals
    Teacher = total_list[-1]["RR"]

    # Create column lists for the student/teacher correlation as well as 
    # average student correlation
    Teacher_corr_column = []
    Student_corr_column = []

    # Calculate the correlations for all participands
    for student in total_list[:-1]:
        Student = student["RR"] # Define the student 
        # Calculate teacher/student correlation
        if df_quiz_list == df_list_quiz_phy:
            # calculate the correlation with max shift on 1 sec
            Teacher_corr_column.append(MaxCorr(Student, Teacher, -1, 1))
        elif df_quiz_list == df_list_quiz_vir:
            # max shift on 60 seconds (1 min)
            Teacher_corr_column.append(MaxCorr(Student, Teacher, -60, 60))
        
        # Calculate average student correlation
        corr_list = []
        for student in total_list[:-1]:
            Student2 = student["RR"]
            if df_quiz_list == df_list_quiz_phy:
                corr = MaxCorr(Student, Student2, -1, 1) # max 1 sec
            elif df_quiz_list == df_list_quiz_vir:
                corr = MaxCorr(Student, Student2, -60, 60) # max 1 min
            corr_list.append(corr)
        # Remove the correlation from the given student to himself
        corr_list = [num for num in corr_list if num < 0.99]
        # Add correlation to the column
        Student_corr_column.append(sum(corr_list)/len(corr_list))
        
    # Add the columns to the dataframe
    df = df_quiz_list[i]
    df["Teacher/Student corr"] = Teacher_corr_column 
    df["Avg. student corr"] = Student_corr_column

# Call the function in order to calculate the correlations for physical and virtual
print("Calculating correlations:")
for i in range(7):
    print("Section: ", i+1, "/ 7")
    Correlations(phy_sections[i], df_list_quiz_phy, i)
for i in range(6):
    print("Section: ", i+1, "/ 6")
    Correlations(vir_sections[i], df_list_quiz_vir, i) 

####################### check results #######################################

# Average                                                    ## Now:##    ## Before:##
print(np.mean(df_list_quiz_phy[3]["Teacher/Student corr"]))  # 0.0332       # 0.1573
print(np.mean(df_list_quiz_phy[3]["Avg. student corr"]))     # 0.0232       # 0.1965

print(np.mean(df_list_quiz_vir[3]["Teacher/Student corr"]))  # 0.1196       # 0.1849 
print(np.mean(df_list_quiz_vir[3]["Avg. student corr"]))     # 0.1330       # 0.1838

# Max
print(np.max(df_list_quiz_phy[3]["Teacher/Student corr"]))   # 0.1379       # 0.2485
print(np.max(df_list_quiz_phy[3]["Avg. student corr"]))      # 0.0543       # 0.2269

print(np.max(df_list_quiz_vir[3]["Teacher/Student corr"]))   # 0.3163       # 0.3163 
print(np.max(df_list_quiz_vir[3]["Avg. student corr"]))      # 0.1528       # 0.2136

# Lists
print(df_list_quiz_phy[3]["Teacher/Student corr"])
print(df_list_quiz_phy[3]["Avg. student corr"])

print(df_list_quiz_vir[3]["Teacher/Student corr"])
print(df_list_quiz_vir[3]["Avg. student corr"])

############### plots ##############
# Teacher/student corr
x_plot_phy = np.arange(0,len(df_list_quiz_phy[3]["Teacher/Student corr"]))
y_plot_phy = df_list_quiz_phy[3]["Teacher/Student corr"]
x_plot_vir = np.arange(0,len(df_list_quiz_vir[3]["Teacher/Student corr"]))
y_plot_vir = df_list_quiz_vir[3]["Teacher/Student corr"]

plt.axhline(y=0, linestyle='dotted', color='gray')  # Add a dotted line at y=0
plt.scatter(x_plot_phy, y_plot_phy, color = "crimson",
                alpha=0.8, label = "Physical")
plt.scatter(x_plot_vir, y_plot_vir, color = "royalblue",
                alpha=0.8, label = "Virtual")
plt.title("Teacher/Student correlations")
plt.xlabel("Student")
plt.ylabel("Correlation")
plt.legend()
plt.show()

# student/student corr
x_plot_phy = np.arange(0,len(df_list_quiz_phy[3]["Avg. student corr"]))
y_plot_phy = df_list_quiz_phy[3]["Avg. student corr"]
x_plot_vir = np.arange(0,len(df_list_quiz_vir[3]["Avg. student corr"]))
y_plot_vir = df_list_quiz_vir[3]["Avg. student corr"]

plt.axhline(y=0, linestyle='dotted', color='gray')  # Add a dotted line at y=0
plt.scatter(x_plot_phy, y_plot_phy, color = "crimson",
                alpha=0.8, label = "Physical")
plt.scatter(x_plot_vir, y_plot_vir, color = "royalblue",
                alpha=0.8, label = "Virtual")
plt.title("Avg. Student correlations")
plt.xlabel("Student")
plt.ylabel("Correlation")
plt.legend()
plt.show()
