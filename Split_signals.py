from Resampling import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled, Cutting,
                        phy_lecture_start_time, phy_lecture_end_time, vir_lecture_start_time, 
                        vir_lecture_end_time, dphy_students, dvir_students, df_quiz_phy, df_quiz_vir)

# Define break start and end time 
phy_break_start_time = datetime.datetime.strptime("21.03.2023 14:11:47", "%d.%m.%Y %H:%M:%S")
phy_break_end_time = datetime.datetime.strptime("21.03.2023 14:27:02", "%d.%m.%Y %H:%M:%S")
vir_break_start_time = datetime.datetime.strptime("28.03.2023 13:55:42", "%d.%m.%Y %H:%M:%S")
vir_break_end_time = datetime.datetime.strptime("28.03.2023 14:14:40", "%d.%m.%Y %H:%M:%S")

# Calculate time before break and after
phy_length_before_break = phy_break_start_time - phy_lecture_start_time # 1:01:47
phy_length_after_break = phy_lecture_end_time - phy_break_end_time # 0:43:09
vir_length_before_break = vir_break_start_time - vir_lecture_start_time # 0:34:17
vir_length_after_break = vir_lecture_end_time - vir_break_end_time # 0:58:57
# We can part the lectures into 14 minutes segments. 
# In that way we only loose the first 5 and last 1 minute of the physical lecture 
# and the first 6 and last 3 minutes of the virtual lecture. That is very good. 

# Define the interval size in minutes
interval_size = 14

# Function to generate timestamps before and after the break
def generate_break_timestamps(lecture_start, lecture_end, break_start, break_end, interval):
    before_break = []
    # Generate timestamps before the break
    current_time = break_start
    while current_time >= lecture_start:
        before_break.insert(0, current_time)
        current_time -= datetime.timedelta(minutes=interval)
    after_break = []
    # Generate timestamps after the break
    current_time = break_end
    while current_time <= lecture_end:
        after_break.append(current_time)
        current_time += datetime.timedelta(minutes=interval)
    return before_break, after_break


# Generate splitting times for each section # Physical
phy_split_before_b = generate_break_timestamps(phy_lecture_start_time, phy_lecture_end_time, 
                                       phy_break_start_time, phy_break_end_time, interval_size)[0]
phy_split_after_b = generate_break_timestamps(phy_lecture_start_time, phy_lecture_end_time, 
                                       phy_break_start_time, phy_break_end_time, interval_size)[1]
# Generate splitting times for each section # Virtual
vir_split_before_b = generate_break_timestamps(vir_lecture_start_time, vir_lecture_end_time, 
                                       vir_break_start_time, vir_break_end_time, interval_size)[0]
vir_split_after_b = generate_break_timestamps(vir_lecture_start_time, vir_lecture_end_time, 
                                       vir_break_start_time, vir_break_end_time, interval_size)[1]

# Function for cutting data into sections
def Cut_sections(before_b, after_b, df_list):
    section_list = []
    for i in range(len(before_b)-1): # Before break
        data = df_list.copy()
        Cutting(before_b[i], before_b[i+1], data)
        section_list.append(data)
    for i in range(len(after_b)-1): # After break
        data = df_list.copy()
        Cutting(after_b[i], after_b[i+1], data)
        section_list.append(data)
    return section_list

phy_sections = Cut_sections(phy_split_before_b, phy_split_after_b, dphy_resampled)
vir_sections = Cut_sections(vir_split_before_b, vir_split_after_b, dvir_resampled)
