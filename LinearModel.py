import pandas
import statistics
from sklearn import linear_model
from sklearn.model_selection import cross_val_predict, LeaveOneOut
from HR_load_and_clean import path
import os

os.chdir(path)

df = pandas.read_csv("merged_stat_data.csv")

column = df['State'].copy()

for i in range(len(column)):
    if column[i] == "Physical":
        column[i] = 1
    else:
        column[i] = 0

df['State'] = column

X = df[['HR_device', 'Number_of_friends', 'State', 'Average_BPM',
       'TeacherStudent_corr', 'Avg_student_corr', 'GC_teacher_to_student',
       'GC_student_to_teacher']]

y = df['Quiz_score']

regr = linear_model.LinearRegression()

predicted = cross_val_predict(regr, X, y, cv = LeaveOneOut())

true_scores = y.values
errors = true_scores - predicted

print(true_scores)
print(predicted)
print(abs(errors))
print("Average error:", statistics.mean(abs(errors)))
print("Standard deviation:", statistics.stdev(abs(errors)))