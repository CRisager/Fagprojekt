#### Wilconxon test - compare physical and virtual ####
# Paired Samples Wilcoxon Test

# The data set
# Physical data frame
file_path <- file.choose("/Users/andreabolvig/Desktop/4.semester/Project work/Fagprojekt_data/phy_stat_data.csv")
physical <- read.csv("file_path")

# Virtual data frame
virtual <-c()
 
# Create a data frame
myData <- data.frame(
phy = rep(c("physical", "virtual"), each = #hvor mange data punkter i hver data frame (skal være ens)),
vir = c(physical, virtual)
)
 
# Print all data
print(myData)
 
# Paired Samples Wilcoxon Test
result = wilcox.test(physical, virtual, paired = TRUE)
 
# Printing the results
print(result)
