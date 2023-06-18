import pandas
import numpy as np

phy_data = pandas.read_csv("/Users/jesperberglund/Downloads/HR_Data/phy_stat_data.csv")
vir_data = pandas.read_csv("/Users/jesperberglund/Downloads/HR_Data/vir_stat_data.csv")

GC_phys_tts = phy_data["GC_teacher_to_student"]
GC_phys_stt = phy_data["GC_student_to_teacher"]
GC_vir_tts = vir_data["GC_teacher_to_student"]
GC_vir_stt = vir_data["GC_student_to_teacher"]

print("Average GC value, physical lecture, teacher to student: ", np.mean(GC_phys_tts))
print("Average GC value, physical lecture, student to teacher: ", np.mean(GC_phys_stt))
print("Average GC value, virtual lecture, teacher to student: ", np.mean(GC_vir_tts))
print("Average GC value, virtual lecture, student to teacher: ", np.mean(GC_vir_stt))

GC_phys_tts_pval = phy_data["GC_ts_pvalue"]
GC_phys_stt_pval = phy_data["GC_st_pvalue"]
GC_vir_tts_pval = vir_data["GC_ts_pvalue"]
GC_vir_stt_pval = vir_data["GC_st_pvalue"]

print("Average p-value, physical lecture, teacher to student: ", np.mean(GC_phys_tts_pval))
print("Average p-value, physical lecture, student to teacher: ", np.mean(GC_phys_stt_pval))
print("Average p-value, virtual lecture, teacher to student: ", np.mean(GC_vir_tts_pval))
print("Average p-value, virtual lecture, student to teacher: ", np.mean(GC_vir_stt_pval))