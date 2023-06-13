from Correlation_calculation import (sns, plt, np, mdates, dphy_resampled, dvir_resampled, phy_sections,
                           vir_sections, df_list_quiz_phy, df_list_quiz_vir, scipy, Correlations)


############## Plot: Correlation as a functions of delay/shift ################################

def corr_as_function_of_delay():
    def corr_delay_entire_vs_section(Student, Teacher, signal_part):
        signal1_norm = (Student-np.mean(Student))/np.std(Student)
        signal2_norm = (Teacher-np.mean(Teacher))/np.std(Teacher)
        # Calculate cross-correlations
        cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
        cross_corr /= len(signal1_norm)
        # Maximum shift is 1 minute
        delays = np.linspace(-(len(Student)-1),len(Teacher)-1,len(cross_corr))
        delays /= 10 # go from samples to seconds. 10 Hz = 10 samples in 1 second

        fig, ax = plt.subplots(1,1)
        plt.plot(delays, cross_corr)
        plt.title("Correlation as a function of delay "+ signal_part)
        plt.xlabel("Delay in seconds")
        plt.ylabel("Correlation")
        plt.show()

    # entire signal
    Student = dphy_resampled[0]["RR"]
    Teacher = dphy_resampled[-1]["RR"]
    corr_delay_entire_vs_section(Student, Teacher, signal_part = "(entire signal)")

    # third section
    Student = phy_sections[3][0]["RR"]
    Teacher = phy_sections[3][-1]["RR"]
    corr_delay_entire_vs_section(Student, Teacher, signal_part = "(one segment)")


    # third section with 1 minute 
    # Define signals 
    signal1 = vir_sections[3][0]["RR"]
    signal2 = vir_sections[3][-1]["RR"]
    # Normalize 
    signal1_norm = (signal1-np.mean(signal1))/np.std(signal1)
    signal2_norm = (signal2-np.mean(signal2))/np.std(signal2)
    # Calculate cross-correlations
    cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
    cross_corr /= len(signal1_norm)
    # Maximum shift is 1 minute
    delays = np.linspace(-(len(signal1)-1),len(signal2)-1,len(cross_corr))
    delays = delays/10
    max_shift_corr = [cross_corr[i] for i in range(len(delays)) if delays[i] > -60 and delays[i] < 60]
    max_shift_delays = [num for num in delays if num > -60 and num < 60]

    fig, ax = plt.subplots(1,1)
    plt.plot(max_shift_delays, max_shift_corr)
    plt.title("Correlation as a function of delay (1 min)")
    plt.xlabel("Delay in seconds")
    plt.ylabel("Correlation")
    plt.show()


    # third section with 1 second 
    # Define signals 
    signal1 = phy_sections[3][0]["RR"]
    signal2 = phy_sections[3][-1]["RR"]
    # Normalize 
    signal1_norm = (signal1-np.mean(signal1))/np.std(signal1)
    signal2_norm = (signal2-np.mean(signal2))/np.std(signal2)
    # Calculate cross-correlations
    cross_corr = scipy.signal.correlate(signal1_norm, signal2_norm, mode="full")
    cross_corr /= len(signal1_norm)
    # Maximum shift is 1 minute
    delays = np.linspace(-(len(signal1)-1),len(signal2)-1,len(cross_corr))
    delays = delays/10
    max_shift_corr = [cross_corr[i] for i in range(len(delays)) if delays[i] >= -1 and delays[i] <= 1]
    max_shift_delays = [num for num in delays if num >= -1 and num <= 1]
    plot_delays = [int(num*1000) for num in max_shift_delays]

    fig, ax = plt.subplots(1,1)
    plt.scatter(plot_delays, max_shift_corr)
    plt.plot(plot_delays, max_shift_corr)
    plt.title("Correlation as a function of delay (1 sec)")
    plt.xlabel("Delay in miliseconds")
    plt.ylabel("Correlation")
    plt.show()
corr_as_function_of_delay()


############## Plot: High vs low correlation ################################

def High_low_corr():
    # Determine the index of the highest and lowest correlations
    max_corr_index = df_list_quiz_phy[0]["Teacher/Student corr"].idxmax()
    min_corr_index = df_list_quiz_phy[0]["Teacher/Student corr"].idxmin()

    # Define teacher and max/min correlation students
    teacher = phy_sections[0][-1]
    min_corr_student = phy_sections[0][min_corr_index]
    max_corr_student = phy_sections[0][max_corr_index]
    # Normalize RR-values
    teacher["RR"] = (teacher["RR"]-np.mean(teacher["RR"]))/np.std(teacher["RR"])
    min_corr_student["RR"] = (min_corr_student["RR"]-np.mean(min_corr_student["RR"]))/np.std(min_corr_student["RR"])
    max_corr_student["RR"] = (max_corr_student["RR"]-np.mean(max_corr_student["RR"]))/np.std(max_corr_student["RR"])

    # Plot of a student with the lowest correlation with teacher
    fig, ax = plt.subplots(1,1)
    sns.lineplot(data = min_corr_student, x="Time", y="RR", color = "crimson", label="student")
    sns.lineplot(data = teacher, x="Time", y="RR", color = "green", label="teacher")
    plt.title("Low correlation")
    plt.legend()
    # format the x-tick labels to only show the time part
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
    plt.show()

    # Plot of a student with the highest correlation with teacher
    fig, ax = plt.subplots(1,1)
    sns.lineplot(data = max_corr_student, x="Time", y="RR", color = "crimson", label="student")
    sns.lineplot(data = teacher, x="Time", y="RR", color = "green", label="teacher")
    plt.title("High correlation")
    plt.legend()
    # format the x-tick labels to only show the time part
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45) # rotate the x-tick labels by 45 degrees
    plt.show()
High_low_corr()


############# Plot: Correlation over time ##################################

def Corr_over_time_phy(section_num, column):
    #### average only
    x_val = np.arange(1,section_num+1)
    y_val = []
    # Add the average teacher/student corr for each section to the y_val list
    for section in df_list_quiz_phy:
        y_val.append(np.mean(section[column]))
    #### all
    x_values = []
    y_values = []
    # Add the average teacher/student corr for each section to the y_val list
    for i, section in enumerate(df_list_quiz_phy):
        x_values.append(np.linspace(i+1-0.2,i+1+0.2,len(section[column])))
        for i in range(len(section[column])):
            y_values.append(section[column][i]) 
    # plot
    fig, ax = plt.subplots(1,1) 
    plt.scatter(x_values, y_values, color = "royalblue", s = 20, alpha = 0.5, label = "All correlations")
    plt.scatter(x_val, y_val, color = "royalblue", s = 45, label = "Avg. correlations")
    plt.plot(x_val, y_val, color = "royalblue")
    plt.axvline(x=4.5, linestyle='dotted', color='gray')  # Add a dotted line to represent the break
    plt.text(0.48, 0.9, "Break", color="gray", transform=ax.transAxes) 
    plt.xlabel("Section")
    plt.ylabel("Correlations")
    plt.title(column + "elation over time")
    plt.legend()
    plt.show()
Corr_over_time_phy(section_num = 7, column = "Teacher/Student corr")
Corr_over_time_phy(section_num = 7, column = "Avg. student corr")


def Corr_over_time_vir(section_num, column):
    #### average only
    x_val = np.arange(1,section_num+1)
    y_val = []
    # Add the average teacher/student corr for each section to the y_val list
    for section in df_list_quiz_vir:
        y_val.append(np.mean(section[column]))
    #### all
    x_values = []
    y_values = []
    # Add the average teacher/student corr for each section to the y_val list
    for i, section in enumerate(df_list_quiz_vir):
        x_values.append(np.linspace(i+1-0.2,i+1+0.2,len(section[column])))
        for i in range(len(section[column])):
            y_values.append(section[column][i]) 
    # plot
    fig, ax = plt.subplots(1,1) 
    plt.scatter(x_values, y_values, color = "firebrick", s = 20, alpha = 0.5, label = "All correlations")
    plt.scatter(x_val, y_val, color = "firebrick", s = 45, label = "Avg. correlations")
    plt.plot(x_val, y_val, color = "firebrick")
    plt.axvline(x=4.5, linestyle='dotted', color='gray')  # Add a dotted line to represent the break
    plt.text(0.5, 0.9, "Break", color="gray", transform=ax.transAxes) 
    plt.xlabel("Section")
    plt.ylabel("Correlations")
    plt.title(column + "elation over time")
    plt.legend()
    plt.show()
Corr_over_time_vir(section_num = 6, column = "Teacher/Student corr")
Corr_over_time_vir(section_num = 6, column = "Avg. student corr")


############# Plot: Permutation ##################################

# permutation 
        



############ Plot: correlation distribution (avg over sections) #######################

# function for calculating average across sections
def Avg_corr(df_list_quiz, column):
    avg_corr_val = []
    for student_index in range(len(df_list_quiz[0])):
        teacher_corr = []
        for section in df_list_quiz:
            teacher_corr.append(section[column][student_index])
        avg_corr_val.append(np.mean(teacher_corr))
    return avg_corr_val


def Distr_of_avg_corr():

    x_plot_phy = np.arange(0,32)
    x_plot_vir = np.arange(0,17)

    def Distr_over_section_avg():
        # Calculate average teacher/student corr
        phy_teacher_corr = Avg_corr(df_list_quiz_phy, column = "Teacher/Student corr")
        vir_teacher_corr = Avg_corr(df_list_quiz_vir, column = "Teacher/Student corr")
        # Plot
        plt.axhline(y=0, linestyle='dotted', color='gray')  # Add a dotted line at y=0
        plt.scatter(x_plot_phy, phy_teacher_corr, color = "royalblue",
                        alpha=0.8, label = "Physical")
        plt.scatter(x_plot_vir, vir_teacher_corr, color = "firebrick",
                        alpha=0.8, label = "Virtual")
        plt.title("Teacher/Student correlations")
        plt.xlabel("Student")
        plt.ylabel("Avg correlation over sections")
        plt.legend()
        plt.show()

        # Calculate average Avg. student corr
        phy_student_corr = Avg_corr(df_list_quiz_phy, column = "Avg. student corr")
        vir_student_corr = Avg_corr(df_list_quiz_vir, column = "Avg. student corr")
        # Plot
        plt.axhline(y=0, linestyle='dotted', color='gray')  # Add a dotted line at y=0
        plt.scatter(x_plot_phy, phy_student_corr, color = "royalblue",
                        alpha=0.8, label = "Physical")
        plt.scatter(x_plot_vir, vir_student_corr, color = "firebrick",
                        alpha=0.8, label = "Virtual")
        plt.title("Avg. Student correlations")
        plt.xlabel("Student")
        plt.ylabel("Correlation")
        plt.legend()
        plt.show()
        return x_plot_phy, x_plot_vir
    Distr_over_section_avg()


    # The datapoints are very clearly seperated so this will be examined further
    phy_list = df_list_quiz_phy.copy()
    vir_list = df_list_quiz_vir.copy()

    #### Avg. student corr ####
    def Avg_student_examination(phy_list, vir_list, x_plot_phy, x_plot_vir):
        # Avg. student corr with max delay for phy and vir = 1 sec
        print("Re-calculating correlations...")
        for section in phy_sections:
            Correlations(section, phy_list, 3, min_phy = -1, min_vir = -1)
        for section in vir_sections:
            Correlations(section, vir_list, 3, min_phy = -1, min_vir = -1) 
        # Average over sections
        phy_student_corr1 = Avg_corr(phy_list, column = "Avg. student corr")
        vir_student_corr1 = Avg_corr(vir_list, column = "Avg. student corr")
        #plot
        plt.axhline(y=0, linestyle='dotted', color='gray')  # Add a dotted line at y=0
        plt.scatter(x_plot_phy, phy_student_corr1, color = "royalblue",
                        alpha=0.8, label = "Physical")
        plt.scatter(x_plot_vir, vir_student_corr1, color = "firebrick",
                        alpha=0.8, label = "Virtual")
        plt.title("Avg. Student correlations (max 1 sec delay for all)")
        plt.xlabel("Student")
        plt.ylabel("Avg correlation over sections")
        plt.legend()
        plt.show()


        # Avg. student corr with max delay for phy and vir = 60 sec
        print("Re-calculating correlations...")
        for section in phy_sections:
            Correlations(section, phy_list, 3, min_phy = -60, min_vir = -60)
        for section in vir_sections:
            Correlations(section, vir_list, 3, min_phy = -60, min_vir = -60) 
        # Average over sections
        phy_student_corr60 = Avg_corr(phy_list, column = "Avg. student corr")
        vir_student_corr60 = Avg_corr(vir_list, column = "Avg. student corr")
        #plot
        plt.axhline(y=0, linestyle='dotted', color='gray')  # Add a dotted line at y=0
        plt.scatter(x_plot_phy, phy_student_corr60, color = "royalblue",
                        alpha=0.8, label = "Physical")
        plt.scatter(x_plot_vir, vir_student_corr60, color = "firebrick",
                        alpha=0.8, label = "Virtual")
        plt.title("Avg. Student correlations (max 60 sec delay for all)")
        plt.xlabel("Student")
        plt.ylabel("Avg correlation over sections")
        plt.legend()
        plt.show()
    Avg_student_examination(phy_list, vir_list, x_plot_phy, x_plot_vir)


    #### Avg. teacher corr #### 
    def Avg_teacher_examination(phy_list, vir_list, x_plot_phy, x_plot_vir):
        # Avg. teacher corr with max delay for phy and vir = 1 sec
        print("Re-calculating correlations...")
        for section in phy_sections:
            Correlations(section, phy_list, 3, min_phy = -1, min_vir = -1)
        for section in vir_sections:
            Correlations(section, vir_list, 3, min_phy = -1, min_vir = -1) 
        # Average over sections
        phy_student_corr1 = Avg_corr(phy_list, column = "Teacher/Student corr")
        vir_student_corr1 = Avg_corr(vir_list, column = "Teacher/Student corr")
        #plot
        plt.axhline(y=0, linestyle='dotted', color='gray')  # Add a dotted line at y=0
        plt.scatter(x_plot_phy, phy_student_corr1, color = "royalblue",
                        alpha=0.8, label = "Physical")
        plt.scatter(x_plot_vir, vir_student_corr1, color = "firebrick",
                        alpha=0.8, label = "Virtual")
        plt.title("Teacher/Student correlations (max 1 sec delay for all)")
        plt.xlabel("Student")
        plt.ylabel("Avg correlation over sections")
        plt.legend()
        plt.show()


        # Avg. teacher corr with max delay for phy and vir = 60 sec
        print("Re-calculating correlations...")
        for section in phy_sections:
            Correlations(section, phy_list, 3, min_phy = -60, min_vir = -60)
        for section in vir_sections:
            Correlations(section, vir_list, 3, min_phy = -60, min_vir = -60) 
        # Average over sections
        phy_student_corr60 = Avg_corr(phy_list, column = "Teacher/Student corr")
        vir_student_corr60 = Avg_corr(vir_list, column = "Teacher/Student corr")
        #plot
        plt.axhline(y=0, linestyle='dotted', color='gray')  # Add a dotted line at y=0
        plt.scatter(x_plot_phy, phy_student_corr60, color = "royalblue",
                        alpha=0.8, label = "Physical")
        plt.scatter(x_plot_vir, vir_student_corr60, color = "firebrick",
                        alpha=0.8, label = "Virtual")
        plt.title("Teacher/Student correlations (max 60 sec delay for all)")
        plt.xlabel("Student")
        plt.ylabel("Avg correlation over sections")
        plt.legend()
        plt.show()
    Avg_teacher_examination(phy_list, vir_list, x_plot_phy, x_plot_vir)
Distr_of_avg_corr()





############# Plot: Variabale relationships ##################################


###############################################################################
############################## NOT DONE #######################################
###############################################################################



# Extract test scores
phy_test_scores = df_list_quiz_phy[0][" Quiz_score"]
vir_test_scores = df_list_quiz_vir[0][" Quiz_score"]


# Calculate average teacher/student corr
phy_teacher_corr = Avg_corr(df_list_quiz_phy, column = "Teacher/Student corr")
vir_teacher_corr = Avg_corr(df_list_quiz_vir, column = "Teacher/Student corr")
# plot
plt.scatter(phy_teacher_corr, phy_test_scores, color = "royalblue",
                alpha=0.8, label = "Physical")
plt.scatter(vir_teacher_corr, vir_test_scores, color = "firebrick",
                alpha=0.8, label = "Virtual")
plt.title("Quiz scores vs teacher/student corr")
plt.xlabel("Avg. teacher/student correlation")
plt.ylabel("Quiz scores")
plt.legend()
plt.show()

# Calculate average Avg. student corr
phy_student_corr = Avg_corr(df_list_quiz_phy, column = "Avg. student corr")
vir_student_corr = Avg_corr(df_list_quiz_vir, column = "Avg. student corr")
# Plot
plt.scatter(phy_student_corr, phy_test_scores, color = "royalblue",
                alpha=0.8, label = "Physical")
plt.scatter(vir_student_corr, vir_test_scores, color = "firebrick",
                alpha=0.8, label = "Virtual")
plt.title("Quiz scores vs teacher/student corr")
plt.xlabel("Avg. student correlation")
plt.ylabel("Quiz scores")
plt.legend()
plt.show()

