#### Wilconxon test - compare physical and virtual ####
# Paired Samples Wilcoxon Test
 
# The data set
# Physical data frame
physical <-c()
 
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
