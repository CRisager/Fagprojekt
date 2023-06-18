from HR_load_and_clean import (path, np, pd, os, plt)
from sklearn import linear_model

# Set directionry to path
os.chdir(path)

# Load the stat data 
phy_data = pd.read_csv('phy_stat_data.csv')
vir_data = pd.read_csv('vir_stat_data.csv')

# Extract GC values
phy_GC_st = phy_data["GC_teacher_to_student"]
phy_GC_ts = phy_data["GC_student_to_teacher"]
vir_GC_st = vir_data["GC_teacher_to_student"]
vir_GC_ts = vir_data["GC_student_to_teacher"]


# Create lists for number of students
phy_students = np.arange(0, len(phy_GC_st))
vir_students = np.arange(0, len(vir_GC_st))


# Plot student->teacher
plt.scatter(phy_students, phy_GC_st, color = "royalblue",
                alpha=0.8, label = "Physical")
plt.scatter(vir_students, vir_GC_st, color = "firebrick",
                alpha=0.8, label = "Virtual")
plt.title("Granger Causality: student -> teacher")
plt.xlabel("Student")
plt.ylabel("Granger Causality values")
plt.legend()
plt.show()


# Plot teacher->student
plt.scatter(phy_students, phy_GC_ts, color = "royalblue",
                alpha=0.8, label = "Physical")
plt.scatter(vir_students, vir_GC_ts, color = "firebrick",
                alpha=0.8, label = "Virtual")
plt.title("Granger Causality: teacher -> student")
plt.xlabel("Student")
plt.ylabel("Granger Causality values")
plt.legend()
plt.show()