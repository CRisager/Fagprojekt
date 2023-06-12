from GrangerCausality import (pd, df_list_quiz_phy, df_list_quiz_vir)


merged_dfs = []

for section_phy, section_vir in enumerate(df_list_quiz_phy[:-1], df_list_quiz_vir):
    # Merge the two dataframes based on the common columns
    merged_dfs.append(pd.merge(section_phy, section_vir, 
                               on=['HR_device', 'Quiz_score', 'Number_of_friends', 
                                   'State', 'Average BPM', 'Teacher/Student corr', 
                                   'Avg. student corr', 'Avg. abs student corr',
                                   "GC student->teacher", "GC teacher->student"]))

