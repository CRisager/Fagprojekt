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
def CrossCorrelation(signal1, signal2):
    # Normalize signals
    signal1_norm = (signal1-np.mean(signal1))/np.std(signal1)
    signal2_norm = (signal2-np.mean(signal2))/np.std(signal2)
    # Calculate cross-correlations (Maximum shift is 1 minute)   
    cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
    cross_corr /= len(cross_corr)
    # Return the maximum correlation
    return np.max(cross_corr)

def Correlations(total_list, df_quiz_list, i):
    # Define the teachers RR-intervals
    Teacher = total_list[-1]["RR"]
    Teacher = (Teacher-np.mean(Teacher))/np.std(Teacher) # Normalize

    # Create column lists for the student/teacher correlation as well as 
    # average student correlation
    Teacher_corr_column = []
    Student_corr_column = []

    # Calculate the correlations for all participands
    student_list = total_list.copy() 
    student_list.pop() # Remove the teacher
    for student in student_list:
        Student = student["RR"] # Define the student
        Student = (Student-np.mean(Student))/np.std(Student) # Normalize
        # Calculate teacher/student correlation
        Teacher_corr_column.append(CrossCorrelation(Student, Teacher)) 
        # Calculate average student correlation
        corr_list = []
        for student in student_list:
            Student2 = student["RR"]
            Student2 = (Student2-np.mean(Student2))/np.std(Student2) # Normalize
            corr = CrossCorrelation(Student, Student2)
            corr_list.append(corr)
        # Remove the correlation from the given student to himself
        corr_list.pop(0)
        # Add correlation to the column
        Student_corr_column.append(sum(corr_list)/len(corr_list))
        
    # Add the columns to the dataframe
    df = df_quiz_list[i]
    print(len(df["Time"]))
    print(len(Teacher_corr_column))
    df["Teacher_Student_corr"] = Teacher_corr_column 
    df["Avg_student_corr"] = Student_corr_column

Correlations(phy_sections[0], df_quiz_phy, 0)

# Call the function in order to calculate the correlations for physical and virtual
for i in range(7):
    Correlations(phy_sections[i], df_quiz_phy, i)
for i in vir_sections:
    Correlations(vir_sections[i], df_quiz_vir, i)

####################### check results #######################################
print(np.max(df_quiz_phy[0]["Teacher/Student corr"]))
print(np.max(df_quiz_phy[0]["Avg. student corr"]))

print(np.max(df_quiz_vir["Teacher/Student corr"]))
print(np.max(df_quiz_vir["Avg. student corr"]))


max_corr_index = df_quiz_phy["Teacher/Student corr"].idxmax()
min_corr_index = df_quiz_phy["Teacher/Student corr"].idxmin()


fig, ax = plt.subplots(1,1)
sns.lineplot(data = dphy_resampled[min_corr_index].iloc[10:], x="Time", y="RR", color = "crimson", label="student")
sns.lineplot(data = dphy_resampled[-1].iloc[10:], x="Time", y="RR", color = "royalblue", label="teacher")
plt.title("Correlation")
plt.legend()
# format the x-tick labels to only show the time part
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
plt.show()


#########################################################################

# Student 1 correlations

# Teacher/student correlation
Student = dphy_resampled[0]["RR"]
Teacher = dphy_resampled[-1]["RR"]

print("Teacher/student correlation: ", CrossCorrelation(Student, Teacher))

# Average student correlation
Student = dphy_resampled[0]["RR"]

corr_list = []
for student in dphy_students:
    Student2 = student["RR"]
    corr = CrossCorrelation(Student, Student2)
    corr_list.append(corr)

corr_list.pop(0)
print("Avg. student correlation: ", sum(corr_list)/len(corr_list))





############## eksempel #####################
signal1_norm = (Student-np.mean(Student))/np.std(Student)
signal2_norm = (Teacher-np.mean(Teacher))/np.std(Teacher)
# Calculate cross-correlations
cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
cross_corr /= len(cross_corr)
# Maximum shift is 1 minute
delays = np.linspace(-(len(Student)-1),len(Teacher)-1,len(cross_corr))

fig, ax = plt.subplots(1,1)
plt.plot(delays, cross_corr)
plt.xlabel("Delay in miliseconds")
plt.ylabel("Correlation")
plt.show()

# Return the maximum correlation
print(np.max(cross_corr))

############## eksempel med correlation med sig selv #####################
signal1_norm = (Student-np.mean(Student))/np.std(Student)
signal2_norm = signal1_norm
# Calculate cross-correlations
cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
cross_corr /= len(cross_corr)
# Maximum shift is 1 minute
delays = np.linspace(-(len(Student)-1),len(Student)-1,len(cross_corr))

fig, ax = plt.subplots(1,1)
plt.plot(delays, cross_corr)
plt.xlabel("Delay in miliseconds")
plt.ylabel("Correlation")
plt.show()

# Return the maximum correlation
print(np.max(cross_corr))














