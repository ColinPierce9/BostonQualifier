import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import numpy
import requests
import io
from loadextract import *
from BQ_ExtractCleanData import *

def etl_bostondata():
    '''
    extract data from Boston Qualifier google sheet
    clean and transform data
    load data to Postgresql database
    '''

    # Use requests to extract data and pandas to convert to dataframe
    response = requests.get('https://docs.google.com/spreadsheets/d/1yc2jk2zv7iSTBSZd_FIU2zNarJ61-GxZTGEs4xr2F_A/export?format=csv')
    assert response.status_code == 200, 'Wrong status code'
    urlData = response.content
    df = pd.read_csv(io.StringIO(urlData.decode('utf-8')),header=2)

    # Clean data to be useful for analysis
    # Rename all features and then make changes to each one
    # Reference notebook for specifics
    df = df.drop(['Name','Want to read more?'],axis=1)
    df = df.rename(columns={'Sex:':'Sex',
                   'Age (at the time of first BQ):':'Age',
                   'Height (in inches):':'Height',
                   'Weight (in lbs at the time of first BQ):':'Weight',
                   'At which marathon did you get your first BQ? ':'First_Marathon',
                   'How long had you been running when you ran your first BQ? ':'Years_Running',
                   'Did you run in college or high school?':'School_Running',
                   'What was your approximate lifetime mileage at the time of your first BQ?':'Lifetime_Mileage',
                   'How many miles did you run in the year before your first BQ?':'Year_Mileage',
                   'Approximately how many races did you run in that year?':'Amount_of_Races',
                   'Did you follow a canned program? ':'Running_Program',
                   'Which one?':'Running_Program_Used',
                   'Did Speed work play a role?':'Speed_Work',
                   'What kind?':'Speed_Work_Used',
                   'Did cross training play a role in your training? If so, how?':'Cross_Training',
                   'What type of cross training':'Cross_Training_Used',
                   'Did you run with a running club or utilize a coach?':'Running_Club_or_Coach'})




    df.reset_index(inplace=True)

    # Sex
    df['Sex'] = df['Sex'].astype(str)
    df['Sex'].replace('m','M',inplace=True)
    df['Sex'].replace('M','Male',inplace=True)
    df['Sex'].replace('f','F',inplace=True)
    df['Sex'].replace('F','Female',inplace=True)

    # Age
    df['Age'] = df['Age'].astype(int)

    # BMI
    df['BMI'] = df['BMI'].round()
    df.loc[236,'Height'] = 68
    df.loc[236,'BMI'] = 22
    df.loc[284,'Height'] = 73
    df.loc[284,'BMI'] = 23

    # First_Marathon
    df['First_Marathon'] = df['First_Marathon'].astype(str)

    # Years_Running
    df['Years_Running'] = df['Years_Running'].replace({'on and off for years':'','9 months':'1','less than a year':'1'})
    df['Years_Running'] = pd.to_numeric(df['Years_Running'])
    df['Years_Running'] = df['Years_Running'].round()

    # School_Running
    df['School_Running'] = df['School_Running'].replace({'n':False,'y':True,'Y':True})

    # Lifetime_Mileage
    df['Lifetime_Mileage'] = df['Lifetime_Mileage'].replace({'?':'','thousand of kms':''})
    df['Lifetime_Mileage'] = df['Lifetime_Mileage'].replace(',','',regex=True)
    df['Lifetime_Mileage'] = pd.to_numeric(df['Lifetime_Mileage'])
    df['Lifetime_Mileage'] = df['Lifetime_Mileage'].round()

    # Year_Mileage
    df['Year_Mileage'] = df['Year_Mileage'].replace('"couple of thousand kms"','')
    df['Year_Mileage'] = pd.to_numeric(df['Year_Mileage'])
    df['Year_Mileage'] = df['Year_Mileage'].round()

    df.loc[129,'Year_Mileage'] = 1400

    # Amount_of_Races
    df['Amount_of_Races'] = df['Amount_of_Races'].replace(2300.0,None)

    # Running_Program
    df['Running_Program'] = df['Running_Program'].replace({'y':True,'n':False,'Y':True})

    # Running_Program_Used
    run_program_df = pd.DataFrame(data=df['Running_Program_Used'])
    run_program_df = run_program_df.dropna()
    run_program_df.reset_index(drop=True,inplace=True)

    total = df['Running_Program_Used'].size
    with_program = run_program_df.size
    without_program = total - with_program

    program_used = pd.DataFrame(data={'Used_Program':[with_program,with_program/total],
                                  'No_Program':[without_program,without_program/total]})
    program_used.index = ['Total','Percent_Total']

    run_program_df['Running_Program_Used'] = run_program_df['Running_Program_Used'].str.lower()

    run_program_df['Running_Program_Used'].replace({'pftizinger 18/55':'pfitz','pftiz':'pfitz','hal hidgon intermediate 2':'higdon',
                                                'run less run faster':'first','run less, run faster':'first',
                                                'faster from 5k to marathon':'Hudson',
                                                "runner's world smart coach":'Runners World Smart Coach',
                                                'runners world':'Runners World Smart Coach','rw run smart':'jack',
                                                ' run with power':'run with power','ha;h hogdon':'higdon'},
                                               inplace=True)

    program_tup_list = [('Nike','nike'),('McMillan','mcmillan'),('McMillan','mcmillian'),('Hal Higdon','higdon'),('Hanson','hanson'),
                ('Pfitzinger','pfitz'),('MY ASICS','asic'),('NY Road Runners','nyrr'),('Boston Athletic Association','baa'),
                ('Jack Daniels','jack'),('FIRST','first'),
                ('Garmin','garmin'),('Baystate Run Program','baystate'),('Cool Running','cool'),('Howard Nippert','nippert'),
                ('Lydiard','lydiard'),('Track Shack','shack'),('Run with Power','run with power'),('Revel Race Series','revel'),
                ("Glover's",'glover')]

    for i,j in program_tup_list:
        run_program_df['Running_Program_Used'] = run_program_df['Running_Program_Used'].apply(lambda x: i if j in x else x)

    program_list = [sub[0] for sub in program_tup_list]

    run_program_df['Running_Program_Used'] = run_program_df[run_program_df['Running_Program_Used'].isin(program_list)]
    run_program_df['Running_Program_Used'].dropna(inplace=True)

    # Speed_Work
    df['Speed_Work'] = df['Speed_Work'].replace({'y':True,'Y':True,'n':False,'N':False})


    # Speed_Work_Used
    speed_work_df = pd.DataFrame(data=df['Speed_Work_Used'])
    speed_work_df = speed_work_df.dropna()
    speed_work_df = speed_work_df.reset_index(drop=True)

    speed_total = df['Speed_Work_Used'].size
    speed_with_program = speed_work_df.size
    speed_without_program = speed_total - speed_with_program

    speed_program_used = pd.DataFrame(data={'Used_Speed_Work':[speed_with_program,speed_with_program/speed_total],
                                  'No_Speed_Work':[speed_without_program,speed_without_program/speed_total]})
    speed_program_used.index = ['Total','Percent_Total']

    speed_work_df['Speed_Work_Used'] = speed_work_df['Speed_Work_Used'].str.lower()

    speed_tup_list = [('Mile Repeats','mile'),
                  ('Tempo Runs','tempo'),
                  ('800m Repeats','800'),
                  ('Marathon Pace','marathon'),
                  ('Yasso 800s','yasso'),
                  ('Fartleks','fartlek'),
                  ('Hill Repeats','hill'),
                  ('400m Repeats','400'),
                  ('Lactate Threshold','threshold'),
                  ('Intervals',('interval','v02 max'))]

    for j,k in speed_tup_list:
        speed_work_df[j] = False
        for i in range(len(speed_work_df['Speed_Work_Used'])-1):

            if type(k) == str:
                if k in speed_work_df['Speed_Work_Used'][i]:
                    speed_work_df[j][i] = True

            else:
                for x in k:
                    if x in speed_work_df['Speed_Work_Used'][i]:
                        speed_work_df[j][i] = True

    speed_list = []
    for i in speed_work_df.columns:
        speed_list.append(i)

    sum_speed_list = []
    speed_list = speed_list[1:]

    for i in speed_list:
        sum_speed_list.append(speed_work_df[i].sum())

    speed_sum_df = pd.DataFrame(list(zip(speed_list,sum_speed_list)),columns=['Speed Work','Sum']).sort_values(by='Sum',ascending=False)

    # Cross_Training
    df['Cross_Training'] = df['Cross_Training'].replace({'y':True,'Y':True,'n':False,'N':False})

    # Cross_Training_Used
    cross_training_df = pd.DataFrame(data=df['Cross_Training_Used'])
    cross_training_df = cross_training_df.dropna()
    cross_training_df = cross_training_df.reset_index(drop=True)

    cross_total = df['Cross_Training_Used'].size
    cross_with = cross_training_df.size
    cross_without = cross_total - cross_with

    cross_training_used = pd.DataFrame(data={'Used_Cross_Training':[cross_with,cross_with/cross_total],
                                  'No_Cross_Training':[cross_without,cross_without/cross_total]})
    cross_training_used.index = ['Total','Percent_Total']

    cross_training_df['Cross_Training_Used'] = cross_training_df['Cross_Training_Used'].str.lower()

    cross_tup_list = [('Swimming','swim'),
                  ('Strength Training',('core','lift','crossfit','weights','weight','trx','erg','row')),
                  ('Rock Climbing','climb'),
                  ('Cycling',('spin','biking','cycling','eliptical','bike')),
                  ('Aerobics',('aerobic','pool')),
                  ('Skiing','ski'),
                  ('Soccer','soccer'),
                  ('Yoga','yoga'),
                  ('Pilates','pilates'),
                  ('MMA','mma'),
                  ('Basketball','basketball'),
                  ('Hockey','hockey'),
                  ('Boot Camp','bootcamp')]

    for j,k in cross_tup_list:
        cross_training_df[j] = False
        for i in range(len(cross_training_df['Cross_Training_Used'])-1):

            if type(k) == str:
                if k in cross_training_df['Cross_Training_Used'][i]:
                    cross_training_df[j][i] = True

            else:
                for x in k:
                    if x in cross_training_df['Cross_Training_Used'][i]:
                        cross_training_df[j][i] = True

    cross_list = []
    for i in cross_training_df.columns:
        cross_list.append(i)

    sum_list = []
    cross_list = cross_list[1:]

    for i in cross_list:
        sum_list.append(cross_training_df[i].sum())

    cross_sum_df = pd.DataFrame(list(zip(cross_list,sum_list)),columns=['Cross_Training','Sum']).sort_values(by='Sum',ascending=False)

    # Running_Club_or_Coach
    df['Running_Club_or_Coach'] = df['Running_Club_or_Coach'].replace({'n':False,'N':False,'y':True,'Y':True})

    # Drop columns
    df2 = df.drop(['Running_Program_Used','Speed_Work_Used','Cross_Training_Used'],axis=1)

    # Transfer each new dataframe to database
    # Tables updated: runner, program, speed, crosstrain
    load_data(df2, 'runner', True)
    load_data(run_program_df, 'program', False)
    load_data(speed_sum_df, 'speed', False)
    load_data(cross_sum_df, 'crosstrain', False)

    print('Boston Qualifier data successfully loaded')
