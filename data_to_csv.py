from GrangerCausality import (pd, np, df_list_quiz_phy, df_list_quiz_vir)

# Define the dataframes from the first section
df_phy = df_list_quiz_phy[0]
df_vir = df_list_quiz_vir[0]

# Only keep the columns that doesn't depend on section and rename columns
phy_csv = pd.DataFrame({"HR_device":df_phy["HR_device"], "Quiz_score":df_phy[" Quiz_score"],
                        "Number_of_friends":df_phy[" Number_of_friends"], "Row_number": df_phy[" Row_number"]
                        , "State":df_phy["State"]})
vir_csv = pd.DataFrame({"HR_device":df_vir["HR_device"], "Quiz_score":df_vir[" Quiz_score"],
                        "Number_of_friends":df_vir[" Number_of_friends"], "State":df_vir["State"]})


# function for calculating average across sections
def Avg_val(df_list_quiz, column): 
    avg_val = []
    for student_index in range(len(df_list_quiz[0])):
        teacher_corr = []
        for section in df_list_quiz:
            teacher_corr.append(section[column][student_index])
        avg_val.append(np.mean(teacher_corr))
    return avg_val 


# Add all the new columns with average over sections to the data frames
# Physical
phy_csv["Average_BPM"] = Avg_val(df_list_quiz_phy, "Average BPM")
phy_csv["TeacherStudent_corr"] = Avg_val(df_list_quiz_phy, "Teacher/Student corr")
phy_csv["Avg_student_corr"] = Avg_val(df_list_quiz_phy, "Avg. student corr")
phy_csv["GC_teacher_to_student"] = Avg_val(df_list_quiz_phy, "GC teacher->student")
phy_csv["GC_student_to_teacher"] = Avg_val(df_list_quiz_phy, "GC student->teacher") 
phy_csv["GC_ts_pvalue"] = Avg_val(df_list_quiz_phy, "GC ts pvalue") 
phy_csv["GC_st_pvalue"] = Avg_val(df_list_quiz_phy, "GC st pvalue") 



# Virtual
vir_csv["Average_BPM"] = Avg_val(df_list_quiz_vir, "Average BPM")
vir_csv["TeacherStudent_corr"] = Avg_val(df_list_quiz_vir, "Teacher/Student corr")
vir_csv["Avg_student_corr"] = Avg_val(df_list_quiz_vir, "Avg. student corr")
vir_csv["GC_teacher_to_student"] = Avg_val(df_list_quiz_vir, "GC teacher->student")
vir_csv["GC_student_to_teacher"] = Avg_val(df_list_quiz_vir, "GC student->teacher") 
vir_csv["GC_ts_pvalue"] = Avg_val(df_list_quiz_vir, "GC ts pvalue") 
vir_csv["GC_st_pvalue"] = Avg_val(df_list_quiz_vir, "GC st pvalue") 

# Create a temporary copy of phy_csv without the "row number" columns
# as phy_csv and vir_csv then have the same columns
phy_csv_temp = phy_csv.drop('Row_number', axis=1)

# Create a merged csv data frame
merged_csv = pd.concat([phy_csv_temp, vir_csv], axis=0) 
                               
                               
# Count the occurrences of each device number
device_counts = merged_csv['HR_device'].value_counts()
# Get the device numbers that appear more than once
multiple_occurrences = device_counts[device_counts > 1].index
# Filter the dataframe to keep only the rows with device numbers that appear more than once
merged_csv = merged_csv[merged_csv['HR_device'].isin(multiple_occurrences)]


# Export the dataframes as csv files
phy_csv.to_csv('phy_stat_data.csv', index=False)
vir_csv.to_csv('vir_stat_data.csv', index=False)
merged_csv.to_csv('merged_stat_data.csv', index=False)