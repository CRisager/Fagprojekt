from HR_load_and_clean import (path, np, pd, os)
from sklearn import linear_model

# Set directionry to path
os.chdir(path)

# Load the merged stat data 
data = pd.read_csv('merged_stat_data.csv')

# Change physical and virtual states to 1 and 0
column = data["State"].copy()
for i in range(len(column)):
    if column[i] == "Physical":
        column[i] = 1
    else:
        column[i] = 0
data["State"] = column

# Separate the predictor variables (X) and the target variable (y)
X = data.drop(['HR_device', 'Quiz_score'], axis=1) # Remove the target variable and HR devices
y = data['Quiz_score']

# Define the model
model = linear_model.LinearRegression()
# Fit the model to the data
model.fit(X, y)


############# Backward selection #############
# the chosen performance metric is R-squared
# The initial R-squared is defined
initial_r_squared = model.score(X, y)
# The initial best R-squared is then that of the full model
best_r_squared = initial_r_squared

# List to track the variables included in the final model
final_variables = list(X.columns)

# Perform backward selection
while True:
    # Define the current best R-squared
    current_r_squared = best_r_squared

    # Remove one variable at a time by the highest p-value (less significant)
    p_values = pd.Series(model.coef_, index=X.columns).abs()  # Exclude the intercept
    if p_values.max() > 0.05:  # Set a significance threshold at alpha = 0.05
        max_p_value_idx = p_values.idxmax() # Find the index of the highest p-value
        X = X.drop(max_p_value_idx, axis=1) # Remove the corresponding variable
        # Fit the model on the new data (without that variable)
        model.fit(X, y)

        # Compare new R-squared with current best R-squared
        if model.score(X, y) < current_r_squared:
            break  # Stop if the performance decreases
        else:
            best_r_squared = model.score(X, y) # Update best R-squared
            # Remove the variable from the final variables list
            final_variables.remove(max_p_value_idx)  
    else:
        break  # Stop if all remaining variables are significant

# Final model summary 
print("\n  Backward selection:")
print("Final R-squared:", best_r_squared)
print("Final Variables:", final_variables)
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)

# Compare R-squared for the full model and final model
print("\nFull model R^2:", initial_r_squared)
print("Best model R^2:", best_r_squared)

"""
Final R-squared: 0.17400827282118092
Final Variables: ['Number_of_friends', 'State', 'Average_BPM', 'TeacherStudent_corr', 'Avg_student_corr', 'GC_teacher_to_student', 'GC_student_to_teacher']
Intercept: 6.130857245304771
Coefficients: [ 1.28748254e+00 -2.47037467e+00  4.23045352e-02 -2.30629677e+01
 -1.49940530e+01 -1.23266171e+03]
 
Full model R^2: 0.17400827282118092
Best model R^2: 0.17400827282118092
"""



########### forward selection ###############
# Separate the predictor variables (X) and the target variable (y)
X = data.drop(['HR_device', 'Quiz_score'], axis=1) # Remove the target variable and HR devices
y = data['Quiz_score']

# Define the model
model = linear_model.LinearRegression()
# Fit the model to the data
model.fit(X, y)

# Set the initial best R-squared
best_r_squared2 = 0
final_variables2 = [] # List for variables in final model

# Perform forward selection
while True:
    # Define the current best R-squared
    current_r_squared = best_r_squared2

    # Create a list of all variables left to add to the model
    remaining_variables = [var for var in X.columns if var not in final_variables2]
    if not remaining_variables:
        break  # Stop if there are no remaining variables

    temp_r_squared = [] # List for R-squared values 

    # Iterate over remaining variables
    for var in remaining_variables:
        temp_variables = final_variables2 + [var] # Add a variable to the model
        X_temp = X[temp_variables] # Edit the data for fitting the model

        # Fit the model
        model.fit(X_temp, y)

        # Add the new R-squared value to the list
        temp_r_squared.append(model.score(X_temp, y))

    # Find the max new R-squared
    max_r_squared = max(temp_r_squared)
    # Determine the variable index corresponding to this best new R-squared
    max_r_squared_idx = temp_r_squared.index(max_r_squared)
    # Compare new best R-squared with the best model R-squared
    if max_r_squared > current_r_squared:
        # Add variable to final model variables list
        selected_variable = remaining_variables[max_r_squared_idx] 
        final_variables2.append(selected_variable)
        best_r_squared2 = max_r_squared # Update best R-squared so far
    else:
        next_best_r_squared = max_r_squared
        break  # Stop if adding more variables doesn't improve performance

# Fit model based on final variables
final_X = X[final_variables2]
model.fit(final_X, y)

# Final model summary
print("\n  Forward selection:")
print("Final R-squared:", best_r_squared2)
print("Final Variables:", final_variables2)
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)

# Compare R-squared for the full model and final model
print("\nFull model R^2:", initial_r_squared)
print("Best model R^2:", best_r_squared2)

""" 
Forward selection:
Final R-squared: 0.17400827282118092
Final Variables: ['GC_teacher_to_student', 'GC_student_to_teacher', 'Number_of_friends', 'State', 'TeacherStudent_corr', 'Average_BPM', 'Avg_student_corr']
Intercept: -3.5625434636763664
Coefficients: [ 5.18810512e+03 -2.78585277e+03  2.03536232e+00 -5.28763899e+00
 -2.03223782e+01  5.53081022e-02 -1.97065589e+00]
 
Full model R^2: 0.17400827282118092
Best model R^2: 0.17400827282118092
"""



