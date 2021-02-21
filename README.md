# BostonQualifier

The Boston Marathon is one of the most popular races in world. Starting in 1897, the race has drawn elite and amateur runners every year to complete the infamous 26.2 miles. 

For runners of all skill levels, qualifing to enter the Boston Marathon is a major accomplishment that takes dedication to achieve. In 2019, the qualifying time for men aged 18-34 was 3hrs 00mins 08secs and for women was 3hrs 30mins 08secs. That's an average mile time of 6:53 and 8:01 respectively over the 26.2 miles. These times seem unimaginable for the non-runner, but these times are designed to be achievable for non-elite runners. The Boston Athletic Association aims to allow the top 5-10% of runners to qualify for the race, but how much training is required to achieve a Boston Qualifing time?

The data for this analysis was obtained from miloandthecalf.com. For the past several years, the site has hosted a questionnaire for athletes that have qualified for the Boston for the first time. This will allow insight into the training habits required to qualify for the race.

### Project

In this project, I've created a pipeline with python in order to store and analyze the data.
- Extract the data from the public google sheet with requests
- Convert to a dataframe to easily clean and transform the data as needed for analysis
- Load data to postgresql database for storage. Database can be accessed for analysis and dashboarding

### Folders

There are two folders in the repository.
- BostonQual-scripts: 
- - BQ_ETL_Main:
- - BQ_ExtactCleanData: 
- - Demo
- BostonQual-notebooks
