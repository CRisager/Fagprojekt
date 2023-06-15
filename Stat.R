#### Set working directory ####
setwd("C:/Users/cheli/OneDrive/Skrivebord/Fagprojekt/Fagprojekt_data")
#setwd("/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data")
#setwd("/Users/jesperberglund/Downloads/HR_data")


#### Load data frames ####
# Physical data frame
physical <- read.table("phy_stat_data.csv", header = TRUE, sep = ",", as.is = TRUE)
# Virtual data frame
virtual <- read.table("vir_stat_data.csv", header = TRUE, sep = ",", as.is = TRUE)
# Merged
merged <- read.table("merged_stat_data.csv", header = TRUE, sep = ",", as.is = TRUE)

# Split the merged dataframe in two, one for phy, one for vir
# where they only contain the students participating in both

# Calculate the midpoint index
midpoint <- nrow(merged) %/% 2
# Split the dataframe into two parts
merged_phy <- merged[1:midpoint, ]
merged_vir <- merged[(midpoint + 1):nrow(merged), ]

# Tjekker om data er normelfordelt ved at bruge KS test
##  H_zero: the data is normal distributed
ks.test(merged_phy$TeacherStudent_corr, "pnorm")
#p-value = 0.0003665
ks.test(merged_vir$TeacherStudent_corr, "pnorm")
#p-value = 6.805e-05
ks.test(merged_phy$Avg_student_corr, "pnorm")
#p-value = 0.0001913
ks.test(merged_vir$Avg_student_corr, "pnorm")
#p-value = 2.813e-05

## The data is not normal distributed because of the small p-value

  
###### Paired Samples Wilcoxon Test ######
TeacherStudentCorr = wilcox.test(merged_phy$TeacherStudent_corr, merged_vir$TeacherStudent_corr, paired = TRUE)
AvgStudentCorr = wilcox.test(merged_phy$Avg_student_corr, merged_vir$Avg_student_corr, paired = TRUE)

#GC_TeacherStudent = wilcox.test(merged_phy$GC_teacher_to_student, merged_vir$GC_teacher_to_student, paired = TRUE)
#GC_StudentTeacher = wilcox.test(merged_phy$GC_student_to_teacher, merged_vir$GC_student_to_teacher, paired = TRUE)

# Printing the results
print(paste("The teacher/student corr p-value is: ", TeacherStudentCorr))
print(paste("The avg. student corr p-value is: ", AvgStudentCorr))

#print(paste("The GC teacher->student p-value is: ", GC_TeacherStudent))
#print(paste("The GC student->teacher p-value is: ", GC_StudentTeacher))

  


###### Multivariable linear model ######

# Physical
phy_fit <- lm(Quiz_score ~ Number_of_friends + Row_number + Average_BPM
+ TeacherStudent_corr + Avg_student_corr + GC_teacher_to_student
+ GC_student_to_teacher, data = physical)
summary(phy_fit)
"""
Residuals:
    Min      1Q  Median      3Q     Max 
-7.2857 -2.1275 -0.1316  2.5723  5.8966 

Coefficients:
                       Estimate Std. Error t value Pr(>|t|)  
(Intercept)             -4.8278     7.2420  -0.667   0.5111  
Number_of_friends        2.5754     1.0386   2.480   0.0202 *
Row_number              -0.4439     0.2519  -1.762   0.0903 .
TeacherStudent_corr     -7.2293    28.9975  -0.249   0.8052  
Avg_student_corr         4.7971    82.1142   0.058   0.9539  
GC_teacher_to_student 3790.3098  2155.4049   1.759   0.0909 .
GC_student_to_teacher -266.9034  1963.7277  -0.136   0.8930  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 3.849 on 25 degrees of freedom
Multiple R-squared:  0.2718,	Adjusted R-squared:  0.09709 
F-statistic: 1.556 on 6 and 25 DF,  p-value: 0.2016

"""

# Virtual
vir_fit <- lm(Quiz_score ~ Number_of_friends + Average_BPM
+ TeacherStudent_corr + Avg_student_corr + GC_teacher_to_student
+ GC_student_to_teacher, data = virtual)
summary(vir_fit)
"""
Residuals:
    Min      1Q  Median      3Q     Max 
-4.1594 -2.8781 -0.1883  1.4213  7.2762 

Coefficients:
                        Estimate Std. Error t value Pr(>|t|)
(Intercept)              -5.8953    22.4827  -0.262    0.798
Number_of_friends         0.7857     2.1464   0.366    0.721
TeacherStudent_corr      -6.5522    30.1175  -0.218    0.832
Avg_student_corr          6.9485   153.0056   0.045    0.965
GC_teacher_to_student  6856.3529  4369.1749   1.569    0.145
GC_student_to_teacher -1777.3028  2047.2862  -0.868    0.404

Residual standard error: 3.987 on 11 degrees of freedom
Multiple R-squared:  0.2128,	Adjusted R-squared:  -0.145 
F-statistic: 0.5946 on 5 and 11 DF,  p-value: 0.7051
"""


# Merged
merged_fit <- lm(Quiz_score ~ Number_of_friends + Average_BPM + State
+ TeacherStudent_corr + Avg_student_corr + GC_teacher_to_student
+ GC_student_to_teacher, data = merged)
summary(merged_fit)
"""
Residuals:
    Min      1Q  Median      3Q     Max 
-7.9991 -2.4470 -0.3816  2.4556  7.5197 

Coefficients:
                        Estimate Std. Error t value Pr(>|t|)  
(Intercept)           -8.850e+00  1.077e+01  -0.822   0.4188  
Number_of_friends      2.035e+00  1.210e+00   1.683   0.1044  
Average_BPM            5.531e-02  9.678e-02   0.572   0.5726  
StateVirtual           5.288e+00  9.558e+00   0.553   0.5849  
TeacherStudent_corr   -2.032e+01  2.491e+01  -0.816   0.4221  
Avg_student_corr      -1.971e+00  8.298e+01  -0.024   0.9812  
GC_teacher_to_student  5.188e+03  2.960e+03   1.753   0.0914 .
GC_student_to_teacher -2.786e+03  1.716e+03  -1.624   0.1165  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 4.092 on 26 degrees of freedom
Multiple R-squared:  0.174,	Adjusted R-squared:  -0.04837 
F-statistic: 0.7825 on 7 and 26 DF,  p-value: 0.6079
"""

# Estimating model parameters (merged)
