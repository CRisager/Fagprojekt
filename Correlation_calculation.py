from Split_signals import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled,
                           dphy_students, dvir_students, phy_sections, vir_sections, df_quiz_phy, df_quiz_vir)
import scipy
from scipy.signal import correlate


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
    delays = np.linspace(-(len(signal1_norm)-1),len(signal2_norm)-1,len(cross_corr))
    shift = int(delays[np.argmax(cross_corr)])
    # Shift the signals accordingly 
    shifted_signal1 = np.roll(signal1_norm, -shift)
    shifted_signal2 = np.roll(signal2_norm, shift)
    # Calculate correlation
    pearson_corr = np.corrcoef(shifted_signal1, shifted_signal2)[0, 1]
    return pearson_corr

def Correlations(total_list, df_quiz_list, i):
    # Define the teachers RR-intervals
    Teacher = total_list[-1]["RR"]

    # Create column lists for the student/teacher correlation as well as 
    # average student correlation
    Teacher_corr_column = []
    Student_corr_column = []

    # Calculate the correlations for all participands
    student_list = total_list.copy() 
    student_list.pop() # Remove the teacher
    for student in student_list:
        Student = student["RR"] # Define the student
        # Calculate teacher/student correlation
        Teacher_corr_column.append(CrossCorrelation(Student, Teacher)) 
        # Calculate average student correlation
        corr_list = []
        for student in student_list:
            Student2 = student["RR"]
            corr = CrossCorrelation(Student, Student2)
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
print("Calculating correlations ...")
for i in range(7):
    Correlations(phy_sections[i], df_list_quiz_phy, i)
for i in range(6):
    Correlations(vir_sections[i], df_list_quiz_vir, i)

####################### check results #######################################
print(np.max(df_list_quiz_phy[0]["Teacher/Student corr"]))
print(np.max(df_list_quiz_phy[0]["Avg. student corr"]))

print(df_list_quiz_phy[0]["Teacher/Student corr"])
print(df_list_quiz_phy[0]["Avg. student corr"])

print(np.max(df_list_quiz_vir[0]["Teacher/Student corr"]))
print(np.max(df_list_quiz_vir[0]["Avg. student corr"]))


max_corr_index = df_list_quiz_phy[0]["Teacher/Student corr"].idxmax()
min_corr_index = df_list_quiz_phy[0]["Teacher/Student corr"].idxmin()

############## Plot: Correlation as a functions of delay/shift ################################

# Teacher/student correlation
Student = dphy_resampled[0]["RR"]
Teacher = dphy_resampled[-1]["RR"]

signal1_norm = (Student-np.mean(Student))/np.std(Student)
signal2_norm = (Teacher-np.mean(Teacher))/np.std(Teacher)
# Calculate cross-correlations
cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
cross_corr /= len(cross_corr)
# Maximum shift is 1 minute
delays = np.linspace(-(len(Student)-1),len(Teacher)-1,len(cross_corr))

fig, ax = plt.subplots(1,1)
plt.plot(delays, cross_corr)
plt.title("Correlation as a function of delay")
plt.xlabel("Delay in miliseconds")
plt.ylabel("Correlation")
plt.show()

############## Plot: High vs low correlation ################################

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
