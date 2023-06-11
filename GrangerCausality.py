from Correlation_calculation import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled,
                           dphy_students, dvir_students, phy_sections, vir_sections, 
                           df_quiz_phy, df_quiz_vir, df_list_quiz_phy, df_list_quiz_vir)
from statsmodels.tsa.stattools import grangercausalitytests
import statistics 
import warnings
import time


def Granger(person1, person2, model_order):
    # Load data
    df = pd.DataFrame({'Person 1': person1["RR"], 'Person 2': person2["RR"]}).reset_index(drop=True)
    data = df.pct_change().dropna() # calculate procental change and remove NaN values if any
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        # fit AR models up to model_order lag
        gc_res = grangercausalitytests(data, model_order, verbose=False)    
    # GC: log of the ratio of variance of residuals between restricted and unrestricted model
    restrict_model = gc_res[model_order][1][0]
    unrestrict_model = gc_res[model_order][1][1]
    variance_of_residuals_restrict = np.var(restrict_model.resid)
    variance_of_residuals_unrestrict = np.var(unrestrict_model.resid)
    GC = np.log(variance_of_residuals_restrict/variance_of_residuals_unrestrict)
    return GC

print("Calculating Granger causality:")
# Calculate Granger causality for physical
granger_list_phys_student_to_teacher = []
granger_list_phys_teacher_to_student = []
for section in phy_sections:
    for student_index, student in enumerate(section[:-1], start=1):
        print("Student", student_index, "/", len(section[:-1])) 
        max_lag = 5*10 # 5 sec react time * sfreq on 10 Hz
        granger_list_phys_student_to_teacher.append(Granger(student, section[-1], max_lag)) # student to teacher
        granger_list_phys_teacher_to_student.append(Granger(section[-1], student, max_lag)) # teacher to student
# Calculate Granger causality for virtual
granger_list_vir_student_to_teacher = []
granger_list_vir_teacher_to_student = []
for section in vir_sections:
    for student_index, student in enumerate(section[:-1], start=1):
        print("Student", student_index, "/", len(section[:-1]))  
        max_lag = (60+5)*10 # (60 sec stream delay + 5 sec react time) * sfreq on 10 Hz
        granger_list_vir_student_to_teacher.append(Granger(student, section[-1], max_lag)) # student to teacher
        granger_list_vir_teacher_to_student.append(Granger(section[-1], student, max_lag)) # teacher to student
        
print(granger_list_phys_student_to_teacher[:5])


#############################################################################################################
########################################## jesper ###########################################################


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




##################################################################################
###################################### test ############################################
import warnings
import time


# Load data
person1 = phy_sections[0][0]
person2 = phy_sections[0][-1]
model_order = 50 
start_time = time.time()
df = pd.DataFrame({'Person 1': person1["RR"], 'Person 2': person2["RR"]}).reset_index(drop=True)
data = df.pct_change().dropna() 
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    gc_res = grangercausalitytests(data, model_order, verbose=False) # fit AR models up to model_order lag
# GC: log of the ratio of variance of residuals between restricted and unrestricted model
max_gc = -float('inf')  # Initialize with negative infinity
max_gc_lag = None
all_gc = []
for lag in gc_res.keys():
    restrict_model = gc_res[lag][1][0]
    unrestrict_model = gc_res[lag][1][1]
    variance_of_residuals_restrict = np.var(restrict_model.resid)
    variance_of_residuals_unrestrict = np.var(unrestrict_model.resid)
    GC = np.log(variance_of_residuals_restrict/variance_of_residuals_unrestrict)
    all_gc.append(GC)
    if GC > max_gc:
        max_gc = GC
        max_gc_lag = lag

print(all_gc)
print(max_gc)
end_time = time.time()
one_calculation = end_time - start_time # 2.8891 s

