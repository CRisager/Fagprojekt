**Welcome!**

This project is a part of a course called "Project Work - Bachelor of Artificial Intelligence and Data" at DTU. It addresses the topic of virtual versus physical lectures. We measured heart rates of students and teacher during both types of lectures, and aim to investigate whether Inter-Subject Correlation of Heart Rate predicts learning experience in a classroom setting.

The heart rate data was obtained using FirstBeat Pro devices and is imported and processed using the scripts in this branch.

**How to run the files**

Firstly, go to HR_load_and_clean.py and input the directory for the data.
All plots and code for this can be found in the "plots" folder.
 - If you want to generate the plots from the data description, run Data_descr_plots.py 
 - If you want to generate the plots from the data analysis, run Correlation_plots.py, Granger_plots.py and Variable_relations.py 
In order to look into our stationarity testing, go to Stationity.py
Before being able to generate the statics, run data_to_csv.py in order to export the calculated data.
Then in order to generate the statics, run Stat.R
