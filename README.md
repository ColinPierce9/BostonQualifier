# Boston Marathon Data Pipeline

The Boston Marathon is one of the most popular races in world. Starting in 1897, the race has drawn elite and amateur runners every year to complete the infamous 26.2 miles. 

For runners of all skill levels, qualifing to enter the Boston Marathon is a major accomplishment that takes dedication to achieve. In 2019, the qualifying time for men aged 18-34 was 3hrs 00mins 08secs and for women was 3hrs 30mins 08secs. That's an average mile time of 6:53 and 8:01 respectively over the 26.2 miles. These times seem unimaginable for the non-runner, but these times are designed to be achievable for non-elite runners. The Boston Athletic Association aims to allow the top 5-10% of runners to qualify for the race, but how much training is required to achieve a Boston Qualifing time?

The data for this analysis was obtained from miloandthecalf.com. For the past several years, the site has hosted a questionnaire for athletes that have qualified for the Boston for the first time. This will allow insight into the training habits required to qualify for the race.

# Project

In this project, I've created a pipeline with python in order to store and analyze the data.
- Extract the data from the public google sheet
- Convert to a dataframe to easily clean and transform the data as needed for analysis
- Load data to postgresql database for storage. Database can be accessed for analysis and dashboarding
- Initial analysis of the data

# Folders

There are two folders in the repository. 'BostonQual-scripts' is for actually initiating the etl pipeline and extracting the clean data for analysis. 'BostonQual-notebooks' is a notebook showing the entire etl process in more detail. This notebook also contains an in depth analysis of the data. These visualizations will eventually be expanded on further. 
- BostonQual-scripts: 
  - BQ_ETL_Main.py: extract data from google sheet, clean and transform data, and load to database 
  - BQ_ExtactCleanData.py: extract clean data from database and returns into a dataframe
  - Demo.ipynb: showcase of how to use these two python scripts
  - loadextract.py: contains the code for working with the database. Note the password is omitted on this repository. 
- BostonQual-notebooks
  - BQ_ETL.ipynb: Full etl pipeline in more detail. Analysis of the data. 
  - loadextract.py: contains the code for working with the database. Note the password is omitted on this repository.


# Future Work
- Create a dashboard containing my analysis to connect with the database. Most likely create my own dashboard with python and django.
- Automate the etl pipeline. Currently, you need to run the python scripts to the extract any new raw data from the source or the clean data from my database. Research the etl workflow tools (likely airflow). 
