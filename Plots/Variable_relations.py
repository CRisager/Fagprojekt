from HR_load_and_clean import (path, np, pd, os, plt)
from sklearn import linear_model

# Set directionry to path
os.chdir(path)

# Load the stat data 
phy_data = pd.read_csv('phy_stat_data.csv')
vir_data = pd.read_csv('vir_stat_data.csv')

print(phy_data.columns)


################### Quiz score vs correlations #######################

# Extract test scores
phy_test_scores = phy_data["Quiz_score"]
vir_test_scores = vir_data["Quiz_score"]


# Extract teacher/student corr
phy_teacher_corr = phy_data["TeacherStudent_corr"]
vir_teacher_corr = vir_data["TeacherStudent_corr"]
# plot 
correlation_phy = np.corrcoef(phy_teacher_corr, phy_test_scores)[0, 1]
text_phy = f"Physical corr = {correlation_phy:.2f}"
correlation_vir = np.corrcoef(vir_teacher_corr, vir_test_scores)[0, 1]
text_vir = f"Virtual corr = {correlation_vir:.2f}"
plt.scatter(phy_teacher_corr, phy_test_scores, color = "royalblue",
                alpha=0.8, label = text_phy)
plt.scatter(vir_teacher_corr, vir_test_scores, color = "firebrick",
                alpha=0.8, label = text_vir)
plt.title("Quiz scores vs teacher/student corr")
plt.xlabel("Teacher/student correlation")
plt.ylabel("Quiz scores")
plt.legend(loc='upper left', facecolor='white', framealpha=0.5)
plt.show()




# Extract Avg. student corr
phy_student_corr = phy_data["Avg_student_corr"]
vir_student_corr = vir_data["Avg_student_corr"]
# plot
correlation_phy = np.corrcoef(phy_student_corr, phy_test_scores)[0, 1]
text_phy = f"Physical corr = {correlation_phy:.2f}"
correlation_vir = np.corrcoef(vir_student_corr, vir_test_scores)[0, 1]
text_vir = f"Virtual corr = {correlation_vir:.2f}"
plt.scatter(phy_student_corr, phy_test_scores, color = "royalblue",
                alpha=0.8, label = text_phy)
plt.scatter(vir_student_corr, vir_test_scores, color = "firebrick",
                alpha=0.8, label = text_vir)
plt.title("Quiz scores vs avg. student correlation")
plt.xlabel("Avg. student correlation")
plt.ylabel("Quiz scores")
plt.legend(loc='upper left', facecolor='white', framealpha=0.5)
plt.show()

################### Correlation vs correlation #######################

# Avg. student corr vs teacher/student corr
# Create a collected list of all teacher/student corr and avg student corr
student_corr = pd.concat([phy_student_corr, vir_student_corr])
teacher_corr = pd.concat([phy_teacher_corr, vir_teacher_corr])
# Calculate the correlation coefficient for the combined group
correlation = np.corrcoef(student_corr, teacher_corr)[0, 1]
text = f"Combined corr = {correlation:.2f}"
# Create the regression line for the combined group
coefficients = np.polyfit(student_corr, teacher_corr, 1)
poly_line = np.poly1d(coefficients)
# Calculate correlation coefficients for each group (phy and vir separately)
correlation_phy = np.corrcoef(phy_student_corr, phy_teacher_corr)[0, 1]
text_phy = f"Physical corr = {correlation_phy:.2f}"
correlation_vir = np.corrcoef(vir_student_corr, vir_teacher_corr)[0, 1]
text_vir = f"Virtual corr = {correlation_vir:.2f}"
# Plot
plt.scatter(phy_student_corr, phy_teacher_corr, color="royalblue", alpha=0.8, label = text_phy)
plt.scatter(vir_student_corr, vir_teacher_corr, color="firebrick", alpha=0.8, label = text_vir)
plt.plot(student_corr, poly_line(student_corr), color="green", linestyle="solid", label = text)
plt.title("Avg. student vs teacher/student corr")
plt.xlabel("Avg. student correlation")
plt.ylabel("Teacher/student corr")
plt.legend()
plt.show()


################### Row number vs correlation #######################

# Teacher/student corr vs row number
# Extract row number
row_num = phy_data["Row_number"]
# Plot phy
correlation_phy = np.corrcoef(phy_teacher_corr, row_num)[0, 1]
text = f"Physical corr = {correlation_phy:.2f}"
# Create a custom legend-like textbox
plt.text(0.05, 0.9, text, transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5'))
plt.scatter(phy_teacher_corr, row_num, color = "royalblue",
                alpha=0.8)
plt.title("Row number vs teacher/student correlation")
plt.xlabel("Teacher/student correlation")
plt.ylabel("Row number")
plt.show()
    
    
    
################### Granger vs correlations #######################

# Extract GC values
phy_GC_st = phy_data["GC_teacher_to_student"]
phy_GC_ts = phy_data["GC_student_to_teacher"]
vir_GC_st = vir_data["GC_teacher_to_student"]
vir_GC_ts = vir_data["GC_student_to_teacher"]

# Create a collected list of all GC teacher->student and student->teacher
GC_ts = pd.concat([phy_GC_ts, vir_GC_ts])
GC_st = pd.concat([phy_GC_st, vir_GC_st])

# plot GC teacher->student vs teacher/student corr
# Calculate the correlation coefficient for the combined group
correlation = np.corrcoef(teacher_corr, GC_ts)[0, 1]
text = f"Combined corr = {correlation:.2f}"
# Correlation coeff phy
correlation_phy = np.corrcoef(phy_teacher_corr, phy_GC_ts)[0, 1]
plt.scatter(phy_teacher_corr, phy_GC_ts, color="royalblue", alpha=0.8,
            label=f"Physical corr = {correlation_phy:.2f}")
# Correlation coeff vir
correlation_vir = np.corrcoef(vir_teacher_corr, vir_GC_ts)[0, 1]
plt.scatter(vir_teacher_corr, vir_GC_ts, color="firebrick", alpha=0.8, 
            label=f"Virtual corr = {correlation_vir:.2f}")
# Create the regression line for the combined group
coefficients = np.polyfit(teacher_corr, GC_ts, 1)
poly_line = np.poly1d(coefficients)
plt.plot(teacher_corr, poly_line(teacher_corr), color="green", 
         linestyle="solid", label = text)
# Plot
plt.title("GC teacher->student vs teacher/student corr")
plt.xlabel("Teacher/student correlation")
plt.ylabel("GC teacher->student values")
plt.legend()
plt.show()





# Calculate the correlation coefficient for the combined group
correlation = np.corrcoef(teacher_corr, GC_st)[0, 1]
text = f"Combined corr = {correlation:.2f}"
# Correlation coeff phy
correlation_phy = np.corrcoef(phy_teacher_corr, phy_GC_st)[0, 1]
plt.scatter(phy_teacher_corr, phy_GC_st, color="royalblue", alpha=0.8,
            label=f"Physical corr = {correlation_phy:.2f}")
# Correlation coeff vir
correlation_vir = np.corrcoef(vir_teacher_corr, vir_GC_st)[0, 1]
plt.scatter(vir_teacher_corr, vir_GC_st, color="firebrick", alpha=0.8, 
            label=f"Virtual corr = {correlation_vir:.2f}")
# Create the regression line for the combined group
coefficients = np.polyfit(teacher_corr, GC_st, 1)
poly_line = np.poly1d(coefficients)
plt.plot(teacher_corr, poly_line(teacher_corr), color="green", 
         linestyle="solid", label = text)
# Plot
plt.title("GC student->teacher vs teacher/student corr")
plt.xlabel("Teacher/student correlation")
plt.ylabel("GC student->teacher values")
plt.legend()
plt.show()