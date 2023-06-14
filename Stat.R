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



  
###### Paired Samples Wilcoxon Test ######
TeacherStudentCorr = wilcox.test(merged_phy$TeacherStudent_corr, merged_vir$TeacherStudent_corr, paired = TRUE)
AvgStudentCorr = wilcox.test(merged_phy$Avg_student_corr, merged_vir$Avg_student_corr, paired = TRUE)
AvgAbsStudentCorr = wilcox.test(merged_phy$Avg_abs_student_corr, merged_vir$Avg_abs_student_corr, paired = TRUE)

#GC_TeacherStudent = wilcox.test(merged_phy$GC_teacher_to_student, merged_vir$GC_teacher_to_student, paired = TRUE)
#GC_StudentTeacher = wilcox.test(merged_phy$GC_student_to_teacher, merged_vir$GC_student_to_teacher, paired = TRUE)

# Printing the results
print(paste("The teacher/student corr p-value is: ", TeacherStudentCorr))
print(paste("The avg. student corr p-value is: ", AvgStudentCorr))
print(paste("The avg. abs student corr p-value is: ", AvgAbsStudentCorr))

#print(paste("The GC teacher->student p-value is: ", GC_TeacherStudent))
#print(paste("The GC student->teacher p-value is: ", GC_StudentTeacher))

  


###### Multivariable linear model ######

# Physical
phy_fit <- lm(Quiz_score ~ Number_of_friends + Row_number + Average_BPM
+ TeacherStudent_corr + Avg_student_corr + Avg_abs_student_corr + GC_teacher_to_student
+ GC_student_to_teacher, data = physical)
summary(phy_fit)
"""
Residuals:
    Min      1Q  Median      3Q     Max 
-7.2480 -2.0770 -0.1134  2.5783  5.9295 

Coefficients:
                       Estimate Std. Error t value Pr(>|t|)  
(Intercept)             -4.0394    11.7951  -0.342   0.7350  
Number_of_friends        2.5749     1.0599   2.429   0.0230 *
Row_number              -0.4446     0.2572  -1.729   0.0967 .
TeacherStudent_corr     -6.4759    30.8674  -0.210   0.8356  
Avg_student_corr         6.7358    86.7901   0.078   0.9388  
Avg_abs_student_corr    -7.6940    89.7134  -0.086   0.9324  
GC_teacher_to_student 3726.4238  2322.2324   1.605   0.1216  
GC_student_to_teacher -269.1580  2004.0866  -0.134   0.8943  
---
Signif. codes:  0 *** 0.001 ** 0.01 * 0.05 . 0.1   1

Residual standard error: 3.928 on 24 degrees of freedom
Multiple R-squared:  0.2721,	Adjusted R-squared:  0.05976 
F-statistic: 1.281 on 7 and 24 DF,  p-value: 0.301
"""

# Virtual
vir_fit <- lm(Quiz_score ~ Number_of_friends + Average_BPM
+ TeacherStudent_corr + Avg_student_corr + Avg_abs_student_corr + GC_teacher_to_student
+ GC_student_to_teacher, data = virtual)
summary(vir_fit)
"""
Residuals:
    Min      1Q  Median      3Q     Max 
-4.5681 -1.6101  0.1536  1.1388  6.2441 

Coefficients:
                      Estimate Std. Error t value Pr(>|t|)  
(Intercept)             57.531     30.916   1.861   0.0924 .
Number_of_friends       -1.410      1.989  -0.709   0.4946  
TeacherStudent_corr    -36.384     29.820  -1.220   0.2504  
Avg_student_corr       113.781    161.022   0.707   0.4959  
Avg_abs_student_corr  -438.245    179.384  -2.443   0.0347 *
GC_teacher_to_student 3465.446   4677.205   0.741   0.4758  
GC_student_to_teacher -288.278   2457.295  -0.117   0.9089  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 3.534 on 10 degrees of freedom
Multiple R-squared:  0.4376,	Adjusted R-squared:  0.1001 
F-statistic: 1.297 on 6 and 10 DF,  p-value: 0.341
"""


# Merged
merged_fit <- lm(Quiz_score ~ Number_of_friends + Average_BPM + State
+ TeacherStudent_corr + Avg_student_corr + Avg_abs_student_corr + GC_teacher_to_student
+ GC_student_to_teacher, data = merged)
summary(merged_fit)
"""
Residuals:
   Min     1Q Median     3Q    Max 
-9.053 -2.318 -0.472  2.161  8.461 

Coefficients:
                        Estimate Std. Error t value Pr(>|t|)
(Intercept)            5.949e+00  1.353e+01   0.440    0.664
Number_of_friends      8.390e-01  1.078e+00   0.779    0.444
Average_BPM            4.489e-02  1.041e-01   0.431    0.670
StateVirtual           4.251e+00  1.171e+01   0.363    0.720
TeacherStudent_corr   -1.675e+01  2.671e+01  -0.627    0.536
Avg_student_corr       3.786e+01  9.196e+01   0.412    0.684
Avg_abs_student_corr  -8.228e+01  9.862e+01  -0.834    0.412
GC_teacher_to_student  1.622e+03  2.623e+03   0.618    0.542
GC_student_to_teacher -1.647e+03  1.786e+03  -0.922    0.365

Residual standard error: 4.292 on 25 degrees of freedom
Multiple R-squared:  0.1264,	Adjusted R-squared:  -0.1532 
F-statistic: 0.4521 on 8 and 25 DF,  p-value: 0.8775
"""

# Estimating model parameters (merged)
