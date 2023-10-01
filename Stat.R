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
GC_ST_PhyVsVir = wilcox.test(merged_phy$GC_student_to_teacher, merged_vir$GC_student_to_teacher, paired = TRUE)$p.value

GC_ST_vs_TS_phy = wilcox.test(merged_phy$GC_student_to_teacher, merged_phy$GC_teacher_to_student, paired = TRUE)$p.value
GC_ST_vs_TS_vir = wilcox.test(merged_vir$GC_student_to_teacher, merged_vir$GC_teacher_to_student, paired = TRUE)$p.value

# Printing the results
print(paste("The test scores p-value is: ", Test_scores))                               # 0.673574611904543 > 0.05
print(paste("The teacher/student corr p-value is: ", TeacherStudentCorr))               # 1.52587890625e-05 < 0.05
print(paste("The avg. student corr p-value is: ", AvgStudentCorr))                      # 1.52587890625e-05 < 0.05
print(paste("The GC teacher->student phy vs vir p-value is: ", GC_TS_PhyVsVir))         # 1.52587890625e-05 < 0.05
print(paste("The GC student->teacher phy vs vir p-value is: ", GC_ST_PhyVsVir))         # 0.0005035         < 0.05
print(paste("The phy GC student->teacher vs other way p-value is: ", GC_ST_vs_TS_phy))  # 0.00933837890625  < 0.05
print(paste("The vir GC student->teacher vs other way p-value is: ", GC_ST_vs_TS_vir))  # 0.430679321289063 > 0.05

print(paste("The Avg. GC teacher->student p-value for phy is: ", mean(physical$GC_ts_pvalue))) # 0.4807 > 0.05
print(paste("The Avg. GC teacher->student p-value for vir is: ", mean(virtual$GC_ts_pvalue)))  # 0.4606 > 0.05
print(paste("The Avg. GC student->teacher p-value for phy is: ", mean(physical$GC_st_pvalue))) # 0.4911 > 0.05
print(paste("The Avg. GC student->teacher p-value for vir is: ", mean(virtual$GC_st_pvalue)))  # 0.5903 > 0.05



###### Perform correlation test #######
## correlations ##
phy_corr_pvalue <- cor.test(physical$TeacherStudent_corr, physical$Avg_student_corr)$p.value
vir_corr_pvalue <- cor.test(virtual$TeacherStudent_corr, virtual$Avg_student_corr)$p.value

# create lists of all needed variables
TS_corrs <- c(physical$TeacherStudent_corr, virtual$TeacherStudent_corr)
SS_corrs <- c(physical$Avg_student_corr, virtual$Avg_student_corr)

corr_pvalue <- cor.test(TS_corrs, SS_corrs)$p.value

# Quiz vs corr
all_quiz <- c(physical$Quiz_score, virtual$Quiz_score)
quiz_ts_corr <- cor.test(TS_corrs, all_quiz)$p.value
quiz_ss_corr <- cor.test(SS_corrs, all_quiz)$p.value
cor.test(physical$TeacherStudent_corr, physical$Quiz_score)$p.value #0.8686716
cor.test(physical$Avg_student_corr, physical$Quiz_score)$p.value #0.364394
cor.test(virtual$TeacherStudent_corr, virtual$Quiz_score)$p.value #0.8463615
cor.test(virtual$Avg_student_corr, virtual$Quiz_score)$p.value #0.6085014


# Print the results 
print(paste("The phy corr p-value is: ", phy_corr_pvalue))   # 0.7410      > 0.05
print(paste("The vir corr p-value is: ", vir_corr_pvalue))   # 0.8332      > 0.05
print(paste("The corr p-value is: ", corr_pvalue))           # 2.41763e-15 < 0.05
print(paste("The quiz vs ts corr p-value is: ", quiz_ts_corr)) # 0.7176    > 0.05
print(paste("The quiz vs ss corr p-value is: ", quiz_ss_corr)) # 0.7500    > 0.05


## Granger ##
phy_gangerTS_pvalue <- cor.test(physical$TeacherStudent_corr, physical$GC_teacher_to_student)$p.value
vir_gangerTS_pvalue <- cor.test(virtual$TeacherStudent_corr, virtual$GC_teacher_to_student)$p.value
phy_gangerST_pvalue <- cor.test(physical$TeacherStudent_corr, physical$GC_student_to_teacher)$p.value
vir_gangerST_pvalue <- cor.test(virtual$TeacherStudent_corr, virtual$GC_student_to_teacher)$p.value

# create lists of all needed variables
TS_values <- c(physical$GC_teacher_to_student, virtual$GC_teacher_to_student)
ST_values <- c(physical$GC_student_to_teacher, virtual$GC_student_to_teacher)

TS_corr_pvalue <- cor.test(TS_corrs, TS_values)$p.value
ST_corr_pvalue <- cor.test(TS_corrs, ST_values)$p.value


# Print the results 
print(paste("The phy granger TS p-value is: ", phy_gangerTS_pvalue))   # 0.3285      > 0.05
print(paste("The vir granger TS p-value is: ", vir_gangerTS_pvalue))   # 0.8665      > 0.05
print(paste("The phy granger ST p-value is: ", phy_gangerST_pvalue))   # 0.0447      < 0.05
print(paste("The vir granger ST p-value is: ", vir_gangerST_pvalue))   # 0.8573      > 0.05

print(paste("The combined TS p-value is: ", TS_corr_pvalue))           # 1.0222e-08  < 0.05
print(paste("The combined ST p-value is: ", ST_corr_pvalue))           # 2.1614e-05  < 0.05






###### Multivariable linear model ######

merged_fit <- lm(Quiz_score ~ Number_of_friends + Average_BPM + merged$State
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
merged$StateVirtual    5.288e+00  9.558e+00   0.553   0.5849  
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

########## With normalized data ############
# Normalize all variables
Quiz_score <- (merged$Quiz_score-mean(merged$Quiz_score))/sd(merged$Quiz_score)
Number_of_friends <- (merged$Number_of_friends-mean(merged$Number_of_friends))/sd(merged$Number_of_friends)
Average_BPM <- (merged$Average_BPM-mean(merged$Average_BPM))/sd(merged$Average_BPM)
TeacherStudent_corr <- (merged$TeacherStudent_corr-mean(merged$TeacherStudent_corr))/sd(merged$TeacherStudent_corr)
Avg_student_corr <- (merged$Avg_student_corr-mean(merged$Avg_student_corr))/sd(merged$Avg_student_corr)
GC_teacher_to_student <- (merged$GC_teacher_to_student-mean(merged$GC_teacher_to_student))/sd(merged$GC_teacher_to_student)
GC_student_to_teacher <- (merged$GC_student_to_teacher-mean(merged$GC_student_to_teacher))/sd(merged$GC_student_to_teacher)

# Fit model
merged_fit2 <- lm(Quiz_score ~ Number_of_friends + Average_BPM + merged$State
                 + TeacherStudent_corr + Avg_student_corr + GC_teacher_to_student
                 + GC_student_to_teacher)
summary(merged_fit2)
"""
Residuals:
     Min       1Q   Median       3Q      Max 
-2.00157 -0.61230 -0.09549  0.61446  1.88160 

Coefficients:
                      Estimate Std. Error t value Pr(>|t|)  
(Intercept)           -0.66154    1.20868  -0.547   0.5888  
Number_of_friends      0.36491    0.21685   1.683   0.1044  
Average_BPM            0.10722    0.18761   0.572   0.5726  
merged$StateVirtual    1.32309    2.39172   0.553   0.5849  
TeacherStudent_corr   -0.32330    0.39635  -0.816   0.4221  
Avg_student_corr      -0.02759    1.16177  -0.024   0.9812  
GC_teacher_to_student  0.84825    0.48397   1.753   0.0914 .
GC_student_to_teacher -0.51057    0.31441  -1.624   0.1165  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 1.024 on 26 degrees of freedom
Multiple R-squared:  0.174,	Adjusted R-squared:  -0.04837 
F-statistic: 0.7825 on 7 and 26 DF,  p-value: 0.6079
"""
