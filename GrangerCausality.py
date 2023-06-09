
from statsmodels.tsa.stattools import grangercausalitytests
import statistics
from Correlation_calculation import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled,
                           dphy_students, dvir_students, phy_sections, vir_sections, 
                           df_quiz_phy, df_quiz_vir, df_list_quiz_phy, df_list_quiz_vir)


lag_phys = 10
lag_vir = 600

# Function to perform Granger Causality from teacher to student in physical lecture
granger_list_phys_teacher_to_student = []
def granger_phys_teacher_to_student(data):
    for section in data:
        for student in section[0:-1]:
            temp_data = pd.DataFrame({"teacher": section[-1]["RR"], "student": student["RR"]})
            result = grangercausalitytests(temp_data, maxlag=lag_phys, verbose=False)
            p_value = result[1][0]['ssr_ftest'][1]
            granger_list_phys_teacher_to_student.append(p_value)

granger_phys_teacher_to_student(phy_sections)

print(statistics.mean(granger_list_phys_teacher_to_student))
print(max(granger_list_phys_teacher_to_student))
print(min(granger_list_phys_teacher_to_student))
print(statistics.median(granger_list_phys_teacher_to_student))

# Function to perform Granger Causality from student to teacher in physical lecture
granger_list_phys_student_to_teacher = []
def granger_phys_student_to_teacher(data):
    for section in data:
        for student in section[0:-1]:
            temp_data = pd.DataFrame({"student": student["RR"], "teacher": section[-1]["RR"]})
            result = grangercausalitytests(temp_data, maxlag=lag_phys, verbose=False)
            p_value = result[1][0]['ssr_ftest'][1]
            granger_list_phys_student_to_teacher.append(p_value)

granger_phys_student_to_teacher(phy_sections)

print(statistics.mean(granger_list_phys_student_to_teacher))
print(max(granger_list_phys_student_to_teacher))
print(min(granger_list_phys_student_to_teacher))
print(statistics.median(granger_list_phys_student_to_teacher))

# Function to perform Granger Causality from teacher to student in virtual lecture
granger_list_vir_teacher_to_student = []
def granger_vir_teacher_to_student(data):
    for section in data:
        for student in section[0:-1]:
            temp_data = pd.DataFrame({"teacher": section[-1]["RR"], "student": student["RR"]})
            result = grangercausalitytests(temp_data, maxlag=lag_vir, verbose=False)
            p_value = result[1][0]['ssr_ftest'][1]
            granger_list_vir_teacher_to_student.append(p_value)

granger_vir_teacher_to_student(vir_sections)

print(statistics.mean(granger_list_vir_teacher_to_student))
print(max(granger_list_vir_teacher_to_student))
print(min(granger_list_vir_teacher_to_student))
print(statistics.median(granger_list_vir_teacher_to_student))

# Function to perform Granger Causality from student to teacher in virtual lecture
granger_list_vir_student_to_teacher = []
def granger_vir_student_to_teacher(data):
    for section in data:
        for student in section[0:-1]:
            temp_data = pd.DataFrame({"student": student["RR"], "teacher": section[-1]["RR"]})
            result = grangercausalitytests(temp_data, maxlag=lag_vir, verbose=False)
            p_value = result[1][0]['ssr_ftest'][1]
            granger_list_vir_student_to_teacher.append(p_value)

granger_vir_student_to_teacher(vir_sections)

print(statistics.mean(granger_list_vir_student_to_teacher))
print(max(granger_list_vir_student_to_teacher))
print(min(granger_list_vir_student_to_teacher))
print(statistics.median(granger_list_vir_student_to_teacher))





'''xlist = np.arange(0,len(granger_list_vir_student_to_teacher))
plt.plot(xlist, granger_list_vir_student_to_teacher)
plt.show()'''


################### Just some tests ###################
test1 = phy_sections[1][16]["RR"]
test2= phy_sections[1][-1]["RR"]
datatest = pd.DataFrame({"student": test1, "teacher": test2})

grangercausalitytests(datatest, maxlag=1)

test3 = phy_sections[1][-1]["RR"]
test4= phy_sections[1][16]["RR"]
datatest = pd.DataFrame({"student": test3, "teacher": test4})

grangercausalitytests(datatest, maxlag=1)

#######################################################

model_order = 4
gc_res = grangercausalitytests(data, model_order) # fit AR models up to model_order lag
# gc_res = grangercausalitytests(data, [model_order]) # fit AR model only using model_order lag
 
# GC: log of the ratio of variance of residuals between restricted and unrestricted model
restrict_model = gc_res[model_order][1][0]
unrestrict_model = gc_res[model_order][1][1]
 
variance_of_residuals_restrict = np.var(restrict_model.resid)
variance_of_residuals_unrestrict = np.var(unrestrict_model.resid)
 
GC = np.log(variance_of_residuals_restrict/variance_of_residuals_unrestrict)
 
print(f"Granger Causality {col_x} to {col_y}: {GC:.3f}")