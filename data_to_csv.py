from GrangerCausality import (pd, np, df_list_quiz_phy, df_list_quiz_vir)

# Define the dataframes from the first section
df_phy = df_list_quiz_phy[0]
df_vir = df_list_quiz_vir[0]

# Only keep the columns that doesn't depend on section and rename columns
phy_csv = pd.DataFrame({"HR device":df_phy["HR_device"], "Quiz score":df_phy[" Quiz_score"],
                        "Number of friends":df_phy[" Number_of_friends"], "Row number": df_phy[" Row_number"]
                        , "State":df_phy["State"]})
vir_csv = pd.DataFrame({"HR device":df_vir["HR_device"], "Quiz score":df_vir[" Quiz_score"],
                        "Number of friends":df_vir[" Number_of_friends"], "State":df_vir["State"]})


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
phy_csv["Average BPM"] = Avg_val(df_list_quiz_phy, "Average BPM")
phy_csv["Teacher/Student corr"] = Avg_val(df_list_quiz_phy, "Teacher/Student corr")
phy_csv["Avg. student corr"] = Avg_val(df_list_quiz_phy, "Avg. student corr")
phy_csv["Avg. abs student corr"] = Avg_val(df_list_quiz_phy, "Avg. abs student corr")
phy_csv["GC teacher->student"] = Avg_val(df_list_quiz_phy, "GC teacher->student")
phy_csv["GC student->teacher"] = Avg_val(df_list_quiz_phy, "GC student->teacher") 

# Virtual
vir_csv["Average BPM"] = Avg_val(df_list_quiz_vir, "Average BPM")
vir_csv["Teacher/Student corr"] = Avg_val(df_list_quiz_vir, "Teacher/Student corr")
vir_csv["Avg. student corr"] = Avg_val(df_list_quiz_vir, "Avg. student corr")
vir_csv["Avg. abs student corr"] = Avg_val(df_list_quiz_vir, "Avg. abs student corr")
vir_csv["GC teacher->student"] = Avg_val(df_list_quiz_vir, "GC teacher->student")
vir_csv["GC student->teacher"] = Avg_val(df_list_quiz_vir, "GC student->teacher") 

# Create a temporary copy of phy_csv without the "row number" columns
# as phy_csv and vir_csv then have the same columns
phy_csv_temp = phy_csv.drop('Row number', axis=1)

# Create a merged csv data frame
merged_csv = pd.concat([phy_csv_temp, vir_csv], axis=0) 
                               
                               
# Count the occurrences of each device number
device_counts = merged_csv['HR device'].value_counts()
# Get the device numbers that appear more than once
multiple_occurrences = device_counts[device_counts > 1].index
# Filter the dataframe to keep only the rows with device numbers that appear more than once
merged_csv = merged_csv[merged_csv['HR device'].isin(multiple_occurrences)]


# Export the dataframes as csv files
phy_csv.to_csv('phy_stat_data.csv', index=False)
vir_csv.to_csv('vir_stat_data.csv', index=False)
merged_csv.to_csv('merged_stat_data.csv', index=False)