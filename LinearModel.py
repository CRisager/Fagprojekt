import pandas
from sklearn import linear_model

df = pandas.read_csv("/Users/jesperberglund/Downloads/HR_Data/merged_stat_data.csv")

column = df['State'].copy()

for i in range(len(column)):
    if column[i] == "Physical":
        column[i] = 1
    else:
        column[i] = 0

df['State'] = column

fit_data = df[:-1]

test_data = df.iloc[-1]

X_train = fit_data[['HR_device', 'Number_of_friends', 'State', 'Average_BPM',
       'TeacherStudent_corr', 'Avg_student_corr', 'GC_teacher_to_student',
       'GC_student_to_teacher']]

y_train = fit_data['Quiz_score']

regr = linear_model.LinearRegression()

X_test = test_data[['HR_device', 'Number_of_friends', 'State', 'Average_BPM',
       'TeacherStudent_corr', 'Avg_student_corr', 'GC_teacher_to_student',
       'GC_student_to_teacher']].values.reshape(1, -1)  # Convert to a 2D array

# Convert back to DataFrame with correct column names
X_test = pandas.DataFrame(X_test, columns=X_train.columns)

y_test = test_data['Quiz_score']

regr.fit(X_train, y_train)

predicted = regr.predict(X_test)

print(predicted)

print("Error:", y_test - predicted)

