from Resampling import (pd, sns, plt, dphy, dvir, datetime, np, start_times_physical, 
start_times_virtual, mdates, dphy_resampled, dvir_resampled, Cutting)


phy_lecture_start_time = datetime.datetime.strptime("21.03.2023 13:10:00", "%d.%m.%Y %H:%M:%S")
phy_break_start_time = datetime.datetime.strptime("21.03.2023 14:11:47", "%d.%m.%Y %H:%M:%S")
phy_length_before_break = phy_break_start_time - phy_lecture_start_time
print(phy_length_before_break)
# 1:01:47

phy_break_end_time = datetime.datetime.strptime("21.03.2023 14:27:02", "%d.%m.%Y %H:%M:%S")
phy_lecture_end_time = datetime.datetime.strptime("21.03.2023 15:10:11", "%d.%m.%Y %H:%M:%S")
phy_length_after_break = phy_lecture_end_time - phy_break_end_time
print(phy_length_after_break)
# 0:43:09

vir_lecture_start_time = datetime.datetime.strptime("28.03.2023 13:21:25", "%d.%m.%Y %H:%M:%S")
vir_break_start_time = datetime.datetime.strptime("28.03.2023 13:55:42", "%d.%m.%Y %H:%M:%S")
vir_length_before_break = vir_break_start_time - vir_lecture_start_time
print(vir_length_before_break)
# 0:34:17

vir_break_end_time = datetime.datetime.strptime("28.03.2023 14:14:40", "%d.%m.%Y %H:%M:%S")
vir_lecture_end_time = datetime.datetime.strptime("28.03.2023 15:13:37", "%d.%m.%Y %H:%M:%S")
vir_length_after_break = vir_lecture_end_time - vir_break_end_time
print(vir_length_after_break)
# 0:58:57

# Physical manual splitting times
phys_starttime1 = datetime.datetime.strptime("21.03.2023 13:15:47", "%d.%m.%Y %H:%M:%S")
phys_starttime2 = datetime.datetime.strptime("21.03.2023 13:29:47", "%d.%m.%Y %H:%M:%S")
phys_starttime3 = datetime.datetime.strptime("21.03.2023 13:43:47", "%d.%m.%Y %H:%M:%S")
phys_starttime4 = datetime.datetime.strptime("21.03.2023 13:57:47", "%d.%m.%Y %H:%M:%S")
phys_endtime4 = phy_break_start_time # 21.03.2023 14:11:47
phys_starttime5 = phy_break_end_time # 21.03.2023 14:27:02
phys_starttime6 = datetime.datetime.strptime("21.03.2023 14:41:02", "%d.%m.%Y %H:%M:%S")
phys_starttime7 = datetime.datetime.strptime("21.03.2023 14:55:02", "%d.%m.%Y %H:%M:%S")
phys_endtime7 = datetime.datetime.strptime("21.03.2023 15:09:02", "%d.%m.%Y %H:%M:%S")

# Virtual manual splitting times
vir_starttime1 = datetime.datetime.strptime("28.03.2023 13:27:42", "%d.%m.%Y %H:%M:%S")
vir_starttime2 = datetime.datetime.strptime("28.03.2023 13:41:42", "%d.%m.%Y %H:%M:%S")
vir_endtime2 = vir_break_start_time # 28.03.2023 13:55:42
vir_starttime3 = vir_break_end_time # 28.03.2023 14:14:40
vir_starttime4 = datetime.datetime.strptime("28.03.2023 14:28:40", "%d.%m.%Y %H:%M:%S")
vir_starttime5 = datetime.datetime.strptime("28.03.2023 14:42:40", "%d.%m.%Y %H:%M:%S")
vir_starttime6 = datetime.datetime.strptime("28.03.2023 14:56:40", "%d.%m.%Y %H:%M:%S")
vir_endtime6 = datetime.datetime.strptime("28.03.2023 15:10:40", "%d.%m.%Y %H:%M:%S")

def Cut_section(start_time, end_time, data, df_list):
    data = df_list.copy()
    Cutting(start_time, end_time, data)
    return data

# Physical
phy_section1 = Cut_section(phys_starttime1, phys_starttime2, dphy_resampled)
phy_section2 = Cut_section(phys_starttime2, phys_starttime3, dphy_resampled)
phy_section3 = Cut_section(phys_starttime3, phys_starttime4, dphy_resampled)
phy_section4 = Cut_section(phys_starttime4, phys_endtime4, dphy_resampled)
phy_section5 = Cut_section(phys_starttime5, phys_starttime6, dphy_resampled)
phy_section6 = Cut_section(phys_starttime6, phys_starttime7, dphy_resampled)
phy_section7 = Cut_section(phys_starttime7, phys_endtime7, dphy_resampled)

# Virtual
vir_section1 = Cut_section(vir_starttime1, vir_starttime2, dvir_resampled)
vir_section2 = Cut_section(vir_starttime2, vir_endtime2, dvir_resampled)
vir_section3 = Cut_section(vir_starttime3, vir_starttime4, dvir_resampled)
vir_section4 = Cut_section(vir_starttime4, vir_starttime5, dvir_resampled)
vir_section5 = Cut_section(vir_starttime5, vir_starttime6, dvir_resampled)
vir_section6 = Cut_section(vir_starttime6, vir_endtime6, dvir_resampled)





