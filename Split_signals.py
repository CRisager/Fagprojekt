from Resampling import (pd, sns, plt, dphy, dvir, datetime, np, start_times_physical, 
start_times_virtual, mdates, dphy_resampled, dvir_resampled, Cutting, phy_lecture_end_time, 
phy_lecture_start_time, vir_lecture_end_time, vir_lecture_start_time)

# Define break start and end time 
phy_break_start_time = datetime.datetime.strptime("21.03.2023 14:11:47", "%d.%m.%Y %H:%M:%S")
phy_break_end_time = datetime.datetime.strptime("21.03.2023 14:27:02", "%d.%m.%Y %H:%M:%S")
vir_break_start_time = datetime.datetime.strptime("28.03.2023 13:55:42", "%d.%m.%Y %H:%M:%S")
vir_break_end_time = datetime.datetime.strptime("28.03.2023 14:14:40", "%d.%m.%Y %H:%M:%S")

dphy_before_break = dphy_resampled.copy()
dphy_after_break = dphy_resampled.copy()
dvir_before_break = dvir_resampled.copy()
dvir_after_break = dvir_resampled.copy()

Cutting(phy_lecture_start_time, phy_break_start_time, dphy_before_break)
Cutting(phy_break_end_time, phy_lecture_end_time, dphy_after_break)

Cutting(vir_lecture_start_time, vir_break_start_time, dvir_before_break)
Cutting(vir_break_end_time, vir_lecture_end_time, dvir_after_break)

