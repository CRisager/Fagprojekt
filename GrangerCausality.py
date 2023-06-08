from Correlation_calculation import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled,
                           dphy_students, dvir_students, phy_sections, vir_sections, 
                           df_quiz_phy, df_quiz_vir, df_list_quiz_phy, df_list_quiz_vir)
from statsmodels.tsa.stattools import grangercausalitytests
import statistics

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

# Function to perform Granger Causality from teacher to student in physical lecture
granger_list_phys_teacher_to_student = []
def granger_phys_teacher_to_student(data):
    for section in data:
        for student in section[0:-1]:
            temp_data = pd.DataFrame({"teacher": section[-1]["RR"], "student": student["RR"]})
            result = grangercausalitytests(temp_data, maxlag=1, verbose=False)
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
            result = grangercausalitytests(temp_data, maxlag=1, verbose=False)
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
            result = grangercausalitytests(temp_data, maxlag=1, verbose=False)
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
            result = grangercausalitytests(temp_data, maxlag=1, verbose=False)
            p_value = result[1][0]['ssr_ftest'][1]
            granger_list_vir_student_to_teacher.append(p_value)

granger_vir_student_to_teacher(phy_sections)

print(statistics.mean(granger_list_vir_student_to_teacher))
print(max(granger_list_vir_student_to_teacher))
print(min(granger_list_vir_student_to_teacher))
print(statistics.median(granger_list_vir_student_to_teacher))


##############################################################
####################### test teacher -> student ##############

######## physical
section = phy_sections[0] # first section
test_list_y = []
for student in section[0:-1]:
    temp_data = pd.DataFrame({"teacher": section[-1]["RR"], "student": student["RR"]})
    result = grangercausalitytests(temp_data, maxlag=1, verbose=False)
    p_value = result[1][0]['ssr_ftest'][1]
    test_list_y.append(p_value)

test_list_x = np.arange(0,len(test_list_y))

plt.scatter(test_list_x,test_list_y)
plt.title("Granger physical distribution")
plt.show()

print("Average: ", np.mean(test_list_y)) # 0.2819
print("Median: ", np.median(test_list_y)) # 0.2020

under_05 = len([num for num in test_list_y if num < 0.05])/len(test_list_y)*100
above_05 = len([num for num in test_list_y if num => 0.05])/len(test_list_y)*100
print("Significant: ", under_05, "%")    # 37.5 % 
print("Unsignificant: ", above_05, "%")  # 62.5 % 


######## virtual
section2 = vir_sections[0] # first section
test_list_y2 = []

for student in section2[0:-1]:
    temp_data = pd.DataFrame({"teacher": section2[-1]["RR"], "student": student["RR"]})
    result = grangercausalitytests(temp_data, maxlag=1, verbose=False)
    p_value = result[1][0]['ssr_ftest'][1]
    test_list_y2.append(p_value)

test_list_x2 = np.arange(0,len(test_list_y2))

print("Average: ", np.mean(test_list_y2)) # 0.1371
print("Median: ", np.median(test_list_y2)) # 0.0046

under_05_2 = len([num for num in test_list_y2 if num < 0.05])/len(test_list_y2)*100
above_05_2 = len([num for num in test_list_y2 if num => 0.05])/len(test_list_y2)*100
print("Significant: ", under_05_2, "%")    # 64.7 %
print("Unsignificant: ", above_05_2, "%")  # 35.2 %




