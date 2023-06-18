from Correlation_calculation import (pd, sns, plt, datetime, np, mdates,
                                     phy_sections, vir_sections, 
                                     df_list_quiz_phy, df_list_quiz_vir, final_stream_delay)
import warnings
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import grangercausalitytests



################## find best model_order #####################################################
# In order to do this, we will use the AIC (Akaike information criterion) value 
# to determine model order resulting in the best fit and complexity

# Function for determining the bst model order 
def best_model_order(person1, person2, max_lag):
    df = pd.DataFrame({'Person 1': person1, 'Person 2': person2}).reset_index(drop=True)
    data = df.pct_change().dropna() # calculate procental change and remove NaN values if any

    all_AIC = [] # list to contain all AIC values
    for i in range(1, max_lag+1): # Loop through possible model orders up to max lag
        model_order = i
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            gc_res = grangercausalitytests(data, model_order, verbose=False) # fit AR models up to model_order lag
        # GC: log of the ratio of variance of residuals between restricted and unrestricted model
        unrestrict_model = gc_res[model_order][1][1]
        # Calculate the AIC
        AIC = unrestrict_model.aic
        all_AIC.append(AIC)

    # Sort the list of all AIC values
    sort_AIC = all_AIC.copy()
    sort_AIC.sort()
    # A difference of 2 or more indicates substantial evidence in favor of the model with the lower AIC
    if sort_AIC[1]-sort_AIC[0] > 2: 
        model_order = all_AIC.index(sort_AIC[0]) # Set the model order from this result
    return model_order


### physical
print("Determining best phy model order for Granger Causality ...")
# Choose two test people for determining the max order (assumes the same for everybody)
Student = phy_sections[0][0]["RR"] # First student in the first section
Teacher = phy_sections[0][-1]["RR"] # The teacher in the first section
max_lag = (1+5)*10 # (1 sec error + 5 sec react time) * sfreq on 10 Hz
# Determine the best model orders (MO) for both student->teacher and teacher->student (these should be the same)
phys_MO_student_teacher = best_model_order(Student, Teacher, max_lag) # 22
phys_MO_teacher_student = best_model_order(Teacher, Student, max_lag) # 19
# Since they in theory should be the same, we'll just use 19
phy_model_order = 22


### virtual
print("Determining best vir model order for Granger Causality ...")
# Choose two test people for determining the max order (assumes the same for everybody)
Student = vir_sections[0][0]["RR"] # First student in the first section
Teacher = vir_sections[0][-1]["RR"] # The teacher in the first section
# The max_lag for vir is (60+5)*10 # (60 sec stream delay + 5 sec react time) * sfreq on 10 Hz
# but this would take forever to run, so we shift the signal according to the calculated stream delay
# and then use the remainding lag as max_lag 
max_lag = 5*10 # 5 sec react time * sfreq on 10 Hz
# Shift one of the signals:
Teacher = np.roll(Teacher,int(final_stream_delay))
# Determine the best model orders (MO) for student->teacher and teacher->student
vir_MO_student_teacher = best_model_order(Student, Teacher, max_lag) # 50 
vir_MO_teacher_student = best_model_order(Teacher, Student, max_lag) # 13
# Since they in theory should be the same, we'll just use 13
vir_model_order = 13




 ####################### Calculate Granger causality ###########################################
 
# Function for calculating granger causality between two people
def Granger(person1, person2, model_order):
    # Load data
    df = pd.DataFrame({'Person 1': person1, 'Person 2': person2}).reset_index(drop=True)
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


# Function for calculate Granger causality for all students in all sections
def GC_for_all(section, df_quiz_list, i, max_lag):
    # Create lists for the GC columns within each section
    gc_teacher_to_student_column = []
    gc_student_to_teacher_column = []
    # Loop over students, calculate GC, add to column lists
    for student_index, student in enumerate(section[:-1], start=1): # loop skips the teacher
        print(student_index, "/", len(section[:-1])) 
        teacher = section[-1]["RR"]
        if df_quiz_list == df_list_quiz_vir:
            teacher = np.roll(teacher,int(final_stream_delay))
        gc_teacher_to_student_column.append(Granger(student["RR"], teacher, max_lag)) # student to teacher
        gc_student_to_teacher_column.append(Granger(teacher, student["RR"], max_lag)) # teacher to student

    # Add the columns to the dataframe
    df = df_quiz_list[i]
    df["GC teacher->student"] = gc_teacher_to_student_column
    df["GC student->teacher"] = gc_student_to_teacher_column


# Call the function in order to calculate the correlations for physical and virtual
print("Calculating Granger causality:")

#max_lag_phy = (1+5)*10 # (1 sec error + 5 sec react time) * sfreq on 10 Hz
for i in range(7): # Phsycial
    print("Section: ", i+1, "/ 7")
    GC_for_all(phy_sections[i], df_list_quiz_phy, i, phy_model_order)
#max_lag_vir = (60+5)*10 # (60 sec stream delay + 5 sec react time) * sfreq on 10 Hz
for i in range(6): # Virtual
    print("Section: ", i+1, "/ 6")
    GC_for_all(vir_sections[i], df_list_quiz_vir, i, vir_model_order) 

