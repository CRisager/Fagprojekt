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

# Function to add average heart rate column
def Average_BPM(sections, df_list_quiz):
    for i in range(len(sections)):
        df = df_list_quiz[i].copy()
        section_column = []
        for student in sections[i][:-1]: # minus the teacher
            section_column.append(np.mean(student["Heart Rate"])) 
        df["Average BPM"] = section_column
        df_list_quiz[i] = df
        
Average_BPM(phy_sections, df_list_quiz_phy)
Average_BPM(vir_sections, df_list_quiz_vir)


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
    best_delay = delays[np.where(cross_corr == max_corr)[0][0]]
    return max_corr, best_delay 

def Correlations(total_list, df_quiz_list, i, min_phy, min_vir):
    # Define the teachers RR-intervals
    Teacher = total_list[-1]["RR"]

    # Create column lists for the student/teacher correlation as well as 
    # average student correlation
    Teacher_corr_column = []
    Student_corr_column = []
    
    # Create a list for best delays in order to determine average stream delay
    stream_delays = []

    # Calculate the correlations for all participands
    for student in total_list[:-1]:
        Student = student["RR"] # Define the student 
        # Calculate teacher/student correlation
        if df_quiz_list == df_list_quiz_phy:
            # calculate the correlation with max shift on 1 sec
            Teacher_corr_column.append(MaxCorr(Student, Teacher, min_phy, abs(min_phy))[0])
        elif df_quiz_list == df_list_quiz_vir:
            # max shift on 60 seconds (1 min)
            Teacher_corr_column.append(MaxCorr(Student, Teacher, min_vir, abs(min_vir))[0])
            stream_delays.append(MaxCorr(Student, Teacher, min_vir, abs(min_vir))[1])
        
        # Calculate average student correlation
        corr_list = []
        for student in total_list[:-1]:
            Student2 = student["RR"]
            if df_quiz_list == df_list_quiz_phy:
                corr = MaxCorr(Student, Student2, min_phy, abs(min_phy))[0] # max 1 sec
            elif df_quiz_list == df_list_quiz_vir:
                corr = MaxCorr(Student, Student2, min_vir, abs(min_vir))[0] # max 1 min
            corr_list.append(corr)
        # Remove the correlation from the given student to himself
        corr_list = [num for num in corr_list if num < 0.99]
        # Add correlation to the column
        Student_corr_column.append(sum(corr_list)/len(corr_list))
        
    # Add the columns to the dataframe
    df = df_quiz_list[i]
    df["Teacher/Student corr"] = Teacher_corr_column 
    df["Avg. student corr"] = Student_corr_column
    
    if df_quiz_list == df_list_quiz_phy:
        stream_delay = None
    else:
        stream_delay = np.mean(stream_delays)
    return stream_delay

# Create a new list for stream delays within each section
stream_delays = []

# Call the function in order to calculate the correlations for physical and virtual
print("Calculating correlations:")
for i in range(7):
    print("Section: ", i+1, "/ 7")
    Correlations(phy_sections[i], df_list_quiz_phy, i, min_phy = -1, min_vir = -60)
for i in range(6):
    print("Section: ", i+1, "/ 6")
    stream_delays.append(Correlations(vir_sections[i], df_list_quiz_vir, i, min_phy = -1, min_vir = -60))

# Remove None values
stream_delays = [num for num in stream_delays if num is not None]
# Calculate the average stream delay across all students and sections
final_stream_delay = np.mean(stream_delays)

