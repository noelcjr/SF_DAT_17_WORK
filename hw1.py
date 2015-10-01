'''
Move this code into your OWN SF_DAT_15_WORK repo
Please complete each question using 100% python code
If you have any questions, ask a peer or one of the instructors!
When you are done, add, commit, and push up to your repo
This is due 7/1/2015
'''


import pandas as pd

# pd.set_option('max_colwidth', 50)
# set this if you need to

killings = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/police-killings.csv')
killings.head()

# 1. Make the following changed to column names:
# lawenforcementagency -> agency
# raceethnicity        -> race
killings.rename(columns={'lawenforcementagency':'agency', 'raceethnicity':'race'}, inplace=True)
# 2. Show the count of missing values in each column
killings.isnull().sum() 
# 3. replace each null value in the dataframe with the string "Unknown"
killings.fillna(value = 'Unknown', inplace = True) 
# 4. How many killings were there so far in 2015? 467
len(killings[killings.year == 2015])
# 5. Of all killings, how many were male and how many female? male 445, female 22
len(killings[killings.gender == 'Male'])
# 6. How many killings were of unarmed people?
len(killings[killings.gender == 'Female'])
# 7. What percentage of all killings were unarmed? 21.84%
from __future__ import division
100*(len(killings[killings.armed == 'No'])/killings.shape[0])
# 8. What are the 5 states with the most killings?
top5_state_killings = sorted(killings.groupby('state').state.count().index[1:5], reverse=True)
top5_numbr_killings = sorted(killings.groupby('state').state.count(), reverse=True)[0:5]
# top5 states by number of killings   = ['CA', 'AZ', 'AR', 'AL']
# number of killings for top 5 states = [74, 46, 29, 25, 22]
# 9. Show a value counts of deaths for each race
killings.groupby('race').race.count()
# race
# Asian/Pacific Islander     10
# Black                     135
# Hispanic/Latino            67
# Native American             4
# Unknown                    15
# White                     236
# 10. Display a histogram of ages of all killings
killings.age.hist(bins=max(killings.age))
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()
# 11. Show 6 histograms of ages by race
killings.age.hist(bins=max(killings.age), by=killings.race, sharex=True, sharey=True)
# 12. What is the average age of death by race?
sum(killings[killings.race == 'Asian/Pacific Islander'].age)/killings.groupby('race').race.count()['Asian/Pacific Islander'] # 40.8 yrs/old
sum(killings[killings.race == 'Black'].age)/killings.groupby('race').race.count()['Black'] # 34.04 yrs/old
sum(killings[killings.race == 'Hispanic/Latino'].age)/killings.groupby('race').race.count()['Hispanic/Latino'] # 34.04 yrs/old
sum(killings[killings.race == 'Native American'].age)/killings.groupby('race').race.count()['Native American'] # 27.75 yrs/old
sum(killings[killings.race == 'Unknown'].age)/killings.groupby('race').race.count()['Unknown']  # 43.53 yrs/old
sum(killings[killings.race == 'White'].age)/killings.groupby('race').race.count()['White'] # 40.47 yrs/old
# 13. Show a bar chart with counts of deaths every month
#KM = killings.groupby('month').month.count() # Plot it and this gives the answer but months are not plot in order
KM = killings['month']
months = ['January','February', 'March','April','May','June','July','August','September','October','November','December']
df_2015_kills_per_month = pd.DataFrame(index=range(1,13), columns=['Month','killings'])
df_2015_kills_per_month['Month'] = months
df_2015_kills_per_month.fillna(0, inplace=True)
index = 1
for i in range(0,len(KM)):
    for j in range(1,13):
        if df_2015_kills_per_month['Month'][j] == KM[i]:
            df_2015_kills_per_month['killings'][i] = df_2015_kills_per_month['killings'][j] + 1
            
df_2015_kills_per_month.plot(kind='bar', title='2015 Killings each month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks([ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],['Jan','Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
plt.show()

###################
### Less Morbid ###
###################

majors = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/college-majors.csv')
majors.head()

# 1. Delete the columns (employed_full_time_year_round, major_code)
del majors['Employed_full_time_year_round']
del majors['Major_code']
# 2. Show the cout of missing values in each column
majors.Major.isnull().sum() # = 0
majors.Major_category.isnull().sum() # = 0
majors.Total.isnull().sum() # = 0
majors.Employed.isnull().sum() # = 0
majors.Unemployed.isnull().sum() # = 0
majors.Unemployment_rate.isnull().sum() # = 0
majors.Median.isnull().sum() # = 0
majors.P25th.isnull().sum() # = 0
majors.P75th.isnull().sum() # = 0
# 3. What are the top 10 highest paying majors?
# I estimated highest pay from the mean of interquartile range
# I belive that is more telling than the median
majors['InterQMean'] = (majors['P75th'] - majors['P25th'])
majors.sort_index(by='InterQMean', ascending=[False]).Major.head(5)
# 4. Plot the data from the last question in a bar chart, include proper title, and labels!
best_paid = majors.sort_index(by='InterQMean', ascending=[False]).head(5)
best_paid['InterQMean'].plot(kind='bar', title='Highest paid majors')
plt.xlabel('Major')
plt.ylabel('Interquartile Mean Salary')
plt.xticks([ 0, 1, 2, 3, 4],['Petroleum Eng.','Math & C.S.','Mining Eng','Pharma','Geology Eng'])
plt.xticks(rotation=10)
# 5. What is the average median salary for each major category?
Meadian_major_category = majors.groupby('Major_category').Median.sum()/majors.groupby('Major_category').Median.count()
# 6. Show only the top 5 paying major categories
Median_major_category.sort()
Median_major_category.tail(5)
Major_category
#Health                     56458.333333
#Business                   60615.384615
#Physical Sciences          62400.000000
#Computers & Mathematics    66272.727273
#Engineering                77758.620690
# 7. Plot a histogram of the distribution of median salaries
majors.Median.hist(bins=10)
plt.xlabel('Median Salaries')
plt.ylabel('Count')
# 8. Plot a histogram of the distribution of median salaries by major category
Meadian_major_category.hist(bins=10)
plt.xlabel('Median Salaries by major category')
plt.ylabel('Count')
# 9. What are the top 10 most UNemployed majors?
# What are the unemployment rates?
major['unemployment_rate'] = (majors['Unemployed']/majors['Employed'])
majors[['Major','unemployment_rate']].sort_index(by='unemployment_rate').tail(10)
#                                        Major  unemployment_rate
#11                               ARCHITECTURE           9.408128
#104                ASTRONOMY AND ASTROPHYSICS           9.411765
#119                         SOCIAL PSYCHOLOGY           9.569378
#19   COMPUTER PROGRAMMING AND DATA PROCESSING           9.922026
#141                VISUAL AND PERFORMING ARTS          10.455497
#77                            LIBRARY SCIENCE          10.478071
#27                  SCHOOL STUDENT COUNSELING          11.327078
#93                      MILITARY TECHNOLOGIES          11.333333
#116                       CLINICAL PSYCHOLOGY          11.446958
#146                   MISCELLANEOUS FINE ARTS          18.504121
##################################################################################
# 10. What are the top 10 most UNemployed majors CATEGORIES? Use the mean for each category
# What are the unemployment rates?
unemployed_majors_category = majors.groupby('Major_category').unemployment_rate.sum()/majors.groupby('Major_category').unemployment_rate.count()
unemployed_majors_category.sort()
unemployed_majors_category.tail(10)
# Major_category
# Physical Sciences                      5.794197
# Industrial Arts & Consumer Services    6.258670
# Computers & Mathematics                6.355489
# Social Science                         7.033380
# Law & Public Policy                    7.287378
# Communications & Journalism            7.434226
# Humanities & Liberal Arts              7.471266
# Interdisciplinary                      8.373943
# Psychology & Social Work               8.462761
# Arts                                   9.711009
# 11. the total and employed column refer to the people that were surveyed.
# Create a new column showing the emlpoyment rate of the people surveyed for each major
# call it "sample_employment_rate"
# Example the first row has total: 128148 and employed: 90245. it's 
# sample_employment_rate should be 90245.0 / 128148.0 = .7042
major['sample_employment_rate'] = (majors['Employed']/majors['Total'])
# 12. Create a "sample_unemployment_rate" colun
# this column should be 1 - "sample_employment_rate"
major['sample_unemployment_rate'] = 1 - major['sample_employment_rate']
