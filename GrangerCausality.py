from statsmodels.tsa.stattools import grangercausalitytests
from Correlation_calculation import (pd, sns, plt, datetime, np, mdates, dphy_resampled, dvir_resampled,
                           dphy_students, dvir_students, phy_sections, vir_sections, 
                           df_quiz_phy, df_quiz_vir, df_list_quiz_phy, df_list_quiz_vir)

# def granger_causation_matrix(data, variables, test="params_ftest", verbose=False):



test1 = phy_sections[1][16]["RR"]
test2= phy_sections[1][-1]["RR"]
datatest = pd.DataFrame({"student": test1, "teacher": test2})

grangercausalitytests(datatest, maxlag=1)

test3 = phy_sections[1][-1]["RR"]
test4= phy_sections[1][16]["RR"]
datatest = pd.DataFrame({"student": test3, "teacher": test4})

grangercausalitytests(datatest, maxlag=1)

for section in phy_sections:
    for student in section:
        print(student["RR"])