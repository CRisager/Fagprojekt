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
# Test scores
Test_scores = wilcox.test(merged_phy$Quiz_score, merged_vir$Quiz_score, paired = TRUE)$p.value
# Correlations
TeacherStudentCorr = wilcox.test(merged_phy$TeacherStudent_corr, merged_vir$TeacherStudent_corr, paired = TRUE)$p.value
AvgStudentCorr = wilcox.test(merged_phy$Avg_student_corr, merged_vir$Avg_student_corr, paired = TRUE)$p.value
# Granger
GC_TS_PhyVsVir = wilcox.test(merged_phy$GC_teacher_to_student, merged_vir$GC_teacher_to_student, paired = TRUE)$p.value

GC_ST_vs_TS_phy = wilcox.test(merged_phy$GC_student_to_teacher, merged_phy$GC_teacher_to_student, paired = TRUE)$p.value
GC_ST_vs_TS_vir = wilcox.test(merged_vir$GC_student_to_teacher, merged_vir$GC_teacher_to_student, paired = TRUE)$p.value

# Printing the results
print(paste("The test scores p-value is: ", Test_scores))                               # 0.673574611904543 > 0.05
print(paste("The teacher/student corr p-value is: ", TeacherStudentCorr))               # 1.52587890625e-05 < 0.05
print(paste("The avg. student corr p-value is: ", AvgStudentCorr))                      # 1.52587890625e-05 < 0.05
print(paste("The GC teacher->student phy vs vir p-value is: ", GC_TS_PhyVsVir))         # 1.52587890625e-05 < 0.05
print(paste("The phy GC student->teacher vs other way p-value is: ", GC_ST_vs_TS_phy))  # 0.00933837890625  < 0.05
print(paste("The vir GC student->teacher vs other way p-value is: ", GC_ST_vs_TS_vir))  # 0.430679321289063 > 0.05

print(paste("The Avg. GC teacher->student p-value for phy is: ", mean(physical$GC_ts_pvalue))) # 0.4807 > 0.05
print(paste("The Avg. GC teacher->student p-value for vir is: ", mean(virtual$GC_ts_pvalue)))  # 0.4606 > 0.05
print(paste("The Avg. GC student->teacher p-value for phy is: ", mean(physical$GC_st_pvalue))) # 0.4911 > 0.05
print(paste("The Avg. GC student->teacher p-value for vir is: ", mean(virtual$GC_st_pvalue)))  # 0.5903 > 0.05





###### Multivariable linear model ######

merged_fit <- lm(Quiz_score ~ Number_of_friends + Average_BPM + State
                 + TeacherStudent_corr + Avg_student_corr + GC_teacher_to_student
                 + GC_student_to_teacher, data = merged)
summary(merged_fit)

""" # nolint
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
