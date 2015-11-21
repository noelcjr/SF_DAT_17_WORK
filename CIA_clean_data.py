# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 14:27:01 2015

@author: Noel Carrascal
@email:  noelcarrascal@gmail.com
"""
import pandas as pd
import numpy as np
import seaborn as sns

cia_fb = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_factbook_table.csv',index_col=[0,1], header=[0, 1, 2]) #, skipinitialspace=True, tupleize_cols=False)

cia_fb.shape  
#  261 x 330 = 86,130 values in the CIA factbook
(cia_fb.isnull().sum().sum()/float(cia_fb.shape[0]*cia_fb.shape[1]))*100
# There are 19,698 null values in the table wich corresponds
# to 22.87% of the values in the table
# We now check the number of nulls adding the nans in each columns
count = 0
for i in cia_fb.columns:
     count = count + cia_fb[i].isnull().sum()
# count = 19698 nulls 
# Same check for rows:
count = 0
for i in cia_fb.index:
    count = count + cia_fb.ix[i].isnull().sum()
# count = 19698
# Get values for fields, categories, years and regions
f = []
c = []
y = []
for i in cia_fb.columns:
    f.append(i[0])
    c.append(i[1])
    y.append(i[2])
fields = set(f)
categories = set(c)
years = set(y)

r = []
for i in cia_fb.index:
    r.append(i[1])
regions = set(r)
# Now get nan values for fields, categories, years and regions
supercount = 0
for i in categories:
    count = 0
    for j in fields:
        count = count + cia_fb[j][i][:].isnull().sum().sum()
    supercount = supercount + count
    print(i,count,supercount)
#    ('Transportation', 1856,  1856)
#    ('Communications', 1805,  3661)
#          ('Military', 1040,  4701)
#('People and Society', 5874, 10575)
#           ('Economy', 8994, 19569)
#         ('Geography',  129, 19698)
supercount = 0
count = 0
for i in fields:
     count = count + cia_fb.xs((i), level=('Field'), axis=1).isnull().sum().sum()
     print(i,cia_fb.xs((i), level=('Field'), axis=1).isnull().sum().sum()) 
#      ('HIV/AIDS - adult prevalence rate', 1034)'People and Soc'
#                                  ('Area',  129)'Geography'
#                              ('Railways', 1394)'Transportation'
#     ('Industrial production growth rate', 1001)'Economy'
#('HIV/AIDS - people living with HIV/AIDS', 1080)'People and Soc'
#         ('GDP (purchasing power parity)',  396)'Economy'
#      ('Inflation rate (consumer prices)',  455)'Economy'
#                               ('Exports',  449)'Economy'
#                ('GDP - per capita (PPP)',  396)'Economy'
#                        ('Internet users',  506)'Communications'
#                        ('Internet hosts',  437)'Communications'
#               ('Current account balance',  914)'Economy'
#                       ('Debt - external',  654)'Economy'
#                     ('HIV/AIDS - deaths', 1210)'People and Soc'
#          ('Telephones - mobile cellular',  464)'Communications'
#                            ('Population',  293)'People and Soc'
#        ('Telephones - main lines in use',  398)'Communications'
#                              ('Roadways',  462)'Transportation'
#                           ('Labor force',  438)'Economy'
#                 ('Military expenditures', 1040)'Military Expen'
#                            ('Death rate',  442)'People and Soc.'
#                           ('Public debt', 1428)'Economy'
#                               ('Imports',  455)'Economy'
#                ('GDP - real growth rate',  516)'Economy'
#                 ('Infant mortality rate',  457)'People and Soc.'
#                            ('Birth rate',  447)'People and Soc.'
#                     ('Unemployment rate',  731)'Economy'
# ('Reserves of foreign exchange and gold', 1161)'Economy'
#                  ('Total fertility rate',  453)'People and Soc.'
#              ('Life expectancy at birth',  458)'People and Soc.'
country_null = []
for i in cia_fb.index:
    country_null.append((i[0],i[1],cia_fb.loc[i[0]].isnull().sum().sum()))
# sorted([country_null,key=lambda x: x[2]]) sort a list of tuples by third item in the tuple
# country_null is a list of tuples with number of null values for each country
#cia_fbT.sortlevel(0) For sorting index
# The Following is a hack for deleting rows of countries it redifines the index
# according to a criteria and re creates the data frame without excluded columns
index2 = []
for i in country_null:
    if (i[2] < 300) & (i[0] != 'World'):
        index2.append((i[0],i[1]))
        
cia_fb2 = pd.DataFrame(cia_fb,index=index2, columns=cia_fb.columns)
# Count = 11855 nan values after deletion
# cia_fb2.shape = (236x330)
# (11855/77880)*100 = 15.22%
cia_fb2.xs(('Transportation'), level=('Category'), axis=1).isnull().sum().sum()
#('Transportation', 1315, 1315)   22 Columns
cia_fb2.xs(('Communications'), level=('Category'), axis=1).isnull().sum().sum()
#('Communications', 768, )  44 Columns
cia_fb2.xs(('Military'), level=('Category'), axis=1).isnull().sum().sum()
#('Military', 772, )   11 Columns
cia_fb2.xs(('People and Society'), level=('Category'), axis=1).isnull().sum().sum()
#('People and Society', 3473, )
cia_fb2.xs(('Economy'), level=('Category'), axis=1).isnull().sum().sum()
#('Economy', 5472, )  143 Columns
cia_fb2.xs(('Geography'), level=('Category'), axis=1).isnull().sum().sum()
#('Geography', 55, )  11 Columns

stat14 = cia_fb2.xs(('Population','People and Society','2014'), level=('Field','Category','Year'), axis=1)
#stat14[('population','People and Society','2014')] = [int(i.replace(",","")) for i in stat14[('Population','People and Society','2014')]]
stat14[('GDP - per capita (PPP)','Economy','2014')] = cia_fb2.xs(('GDP - per capita (PPP)','Economy','2014'), level=('Field','Category','Year'), axis=1)
stat14[('GDP - per capita (PPP)','Economy','2014')].fillna(-1, inplace=True)
#stat14[('gdp_pc','Economy','2014')] = [int(i.replace(",","")) for i in stat14[('GDP - per capita (PPP)','Economy','2014')]]
stat14[('Nulls','Number per country','2014')] = [cia_fb2.loc[i[0]].isnull().sum().sum() for i in cia_fb2.index]
stat14.dtypes
stat14 = stat14[[('Population','People and Society','2014'),('GDP - per capita (PPP)','Economy','2014'),('Nulls','Number per country','2014')]]
stat14.sort(columns=(('Population','People and Society','2014')), axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last')
''' The following loop shows population, gdp per capita and number of nulls. To select elimination criteria'''
country_in = []
count = 1
for i in stat14.index:
     # The following if eliminates 38 countries that are too small and with low economic impact to be statistically significant 
     if stat14.ix[i[0]][('Population','People and Society','2014')][0] < 150000 and stat14.ix[i[0]][('GDP - per capita (PPP)','Economy','2014')][0] < 35000:
         print('Eliminated',count,i[0])
         count = count + 1
     else:
         country_in.append((i[0],i[1]))
 
cia_fb3 = pd.DataFrame(cia_fb,index=country_in, columns=cia_fb.columns)
# Count = 6495 nan values after deletion
# cia_fb2.shape = (200x330)
# (6495/77880)*100 = 8.34%
cia_fb3.xs(('Transportation'), level=('Category'), axis=1).isnull().sum().sum()
#('Transportation', 835, 835)   22 Columns
cia_fb3.xs(('Communications'), level=('Category'), axis=1).isnull().sum().sum()
#('Communications', 320, )  44 Columns
cia_fb3.xs(('Military'), level=('Category'), axis=1).isnull().sum().sum()
#('Military', 398, )   11 Columns
cia_fb3.xs(('People and Society'), level=('Category'), axis=1).isnull().sum().sum()
#('People and Society', 1709, )
cia_fb3.xs(('Economy'), level=('Category'), axis=1).isnull().sum().sum()
#('Economy', 3196, )  143 Columns
cia_fb3.xs(('Geography'), level=('Category'), axis=1).isnull().sum().sum()
#('Geography', 37, )  11 Columns  
list_tuples = [('Geography','Area'), 
               ('Economy','Industrial production growth rate'), \
               ('Economy','GDP (purchasing power parity)'), \
               ('Economy','Inflation rate (consumer prices)'), \
               ('Economy','Exports'), \
               ('Economy','GDP - per capita (PPP)'), \
               ('Economy','Current account balance'), \
               ('Economy','Debt - external'), \
               ('Economy','Labor force'), \
               ('Economy','Public debt'), \
               ('Economy','Imports'), \
               ('Economy','GDP - real growth rate'), \
               ('Economy','Unemployment rate'), \
               ('Economy','Reserves of foreign exchange and gold'), \
               ('Communications','Internet users'), \
               ('Communications','Internet hosts'), \
               ('Communications','Telephones - mobile cellular'), \
               ('Communications','Telephones - main lines in use'), \
               ('Transportation','Roadways'), \
               ('Transportation','Railways'), \
               ('Military','Military expenditures'), \
               ('People and Society','Death rate'), \
               ('People and Society','Infant mortality rate'), \
               ('People and Society','Birth rate'), \
               ('People and Society','Total fertility rate'), \
               ('People and Society','Life expectancy at birth'), \
               ('People and Society','Population'), \
               ('People and Society','HIV/AIDS - deaths'), \
               ('People and Society','HIV/AIDS - people living with HIV/AIDS'), \
               ('People and Society','HIV/AIDS - adult prevalence rate')]
null_index = []
for i in categories:
     for j in fields:
         null_index.append((i,j))
years = [2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
null_heatmap = pd.DataFrame(index=list_tuples, columns=years)
null_heatmap.index = pd.MultiIndex.from_tuples(list_tuples, names=['Category','Field'])
null_heatmap.fillna(0, inplace=True)

for i in list_tuples:
    for j in years:
        null_heatmap.ix[(i[0],i[1])][j] = cia_fb3.xs((i[0],i[1],str(j)), level=('Category','Field','Year'), axis=1).isnull().sum().sum()

sns.heatmap(null_heatmap)  
    
cia_fb3.to_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_factbook_200_countries_table.csv')
