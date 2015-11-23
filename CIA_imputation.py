# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:24:45 2015
@author: noelcjr
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#cia_200fb = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_factbook_200_countries_table.csv',index_col=[0,1], header=[0, 1, 2]) #, skipinitialspace=True, tupleize_cols=False)
#cia_200fb.isnull().sum().sum() # = 6495
cia_fb = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_factbook_table.csv',index_col=[0,1], header=[0, 1, 2]) #, skipinitialspace=True, tupleize_cols=False)

EU = ['Austria','Belgium','Bulgaria','Cyprus','Croatia','Czech Republic', \
'Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland', \
'Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland', \
'Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','United Kingdom']

years = [2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
              
new_tuples_cols = []
stats_on_field = ['nulls','a1','b1','2014','a2','b2','2013']
for i in cia_fb.columns:
    for j in stats_on_field:
        new_tuples_cols.append((i[1],i[0],j))

new_tuples_index = []
for i in cia_fb.index:                                                # Change cia_fb to cia_200fb
    new_tuples_index.append((i[0],i[1]))
    
countries_lr_stats = pd.DataFrame(index=cia_fb.index, columns=new_tuples_cols)  # Change cia_fb to cia_200fb
countries_lr_stats.columns=pd.MultiIndex.from_tuples(new_tuples_cols, names=['Field','Category','Stats'])
# The following line flatens a multi index dataframe
# testPDF.columns = [' @ '.join(col).strip() for col in testPDF.columns.values]
supercount = 0
for i in cia_fb.columns:
    temp = cia_fb.xs((i[0],i[1]), level=('Field','Category'), axis=1)   # Change cia_fb to cia_200fb
    for j in range(0,len(temp)):
        c = pd.DataFrame(temp.ix[j])
        c.columns = ['value']
        nulls = c['value'].isnull().sum()
        nulls2 =  c['value'][1:len(c)].isnull().sum()
        #Keep track, then eliminate nulls before linear regression
        #After regression use cnull to predict values for missing data.
        countries_lr_stats.ix[temp.index[j]][(i[1],i[0],'nulls')] = int(nulls)
        cnull = c.isnull()
        cnull['year'] = cnull.index
        c.dropna(inplace=True)
        if nulls < 10:
            c['year'] = c.index
            # Fix types to be able to do linear regression
            if isinstance(c['value'][0], str):
                c['value'] = [n.replace(",","") for n in c['value']]
            c[['value']] = c[['value']].astype(float)
            c[['year']] = c[['year']].astype(int)
            feature_cols = ['year']
            X = c[feature_cols]
            y = c.value
            # instantiate and fit
            linreg = LinearRegression()
            linreg.fit(X, y)
            countries_lr_stats.ix[temp.index[j]][(i[1],i[0],'a1')] = float(linreg.coef_)
            countries_lr_stats.ix[temp.index[j]][(i[1],i[0],'b1')] = float(linreg.intercept_)
            val = linreg.predict(2014)[0]
            countries_lr_stats.ix[temp.index[j]][(i[1],i[0],'2014')] = float(val)
            #With All null values eliminated and linear regressions calculated... move on to fill in missing values in original
            #cia factbook data.
            count = 0
            for k in cnull['value']:
                if k:
                    cia_fb.loc[temp.index[j],(i[0],i[1],cnull.year[str(years[count])])] = float(linreg.predict(years[count])[0]) # Change cia_fb to cia_200fb
                    #print('Null:',temp.index[j],years[count])
                    supercount = supercount + 1
                count = count + 1
            if nulls2 < 9:  # This means that 2014 is not null and we can do the linear regression upto 2013, and estimate 2014
                linreg2 = LinearRegression()
                linreg2.fit(X[1:len(X)],y[1:len(y)])
                countries_lr_stats.ix[temp.index[j]][(i[1],i[0],'a2')] = float(linreg2.coef_)
                countries_lr_stats.ix[temp.index[j]][(i[1],i[0],'b2')] = float(linreg2.intercept_)
                val2 = linreg2.predict(2014)[0]
                countries_lr_stats.ix[temp.index[j]][(i[1],i[0],'2013')] = float(val2)

cia_fb.isnull().sum().sum()
# 16719
# NULLS by country
# Get rid of Oceans, Poles, World, territories, and Fill Up European Union from countries
# Create heat map with nullvalues per fields. After I regularize the data, I could discard
# some fields with redundant or many null Values.
country_null = []
for i in cia_fb.index:
    country_null.append((i[0],i[1],cia_fb.loc[i[0]].isnull().sum().sum()))

#NULSS by field
count = 0
for i in fields:
     count = count + cia_fb.xs((i), level=('Field'), axis=1).isnull().sum().sum()
     print(i,cia_fb.xs((i), level=('Field'), axis=1).isnull().sum().sum(),count) 

catss = ['Geography','Economy','Communications','Transportation','Military','People and Society']
for i in catss:
    temp = cia_fb.xs((i), level=('Category'), axis=1)   # Change cia_fb to cia_200fb
    print(i,temp.isnull().sum().sum())

cia_fb2  = cia_fb
cia_fb2 = cia_fb.dropna()          # Change cia_fb to cia_200fb
(cia_fb2[('Population','People and Society','2014')].sum()/cia_fb[('Population','People and Society','2014')].sum())*100  # Change cia_fb to cia_200fb
(cia_fb2[('GDP (purchasing power parity)','Economy','2014')].sum()/cia_fb[('GDP (purchasing power parity)','Economy','2014')].sum())*100  # Change cia_fb to cia_200fb
# FAILS AT: cia_200fb.ix[('United States', 'North America')][('Area','Geography','2014')]
           
# WARNING temp.ix[temp.index[100] has weird values from 2005 and 2004 Economy Industrial production growth rate.
#null_country_heatmap = []
#null_country_heatmap = pd.DataFrame(index=cia_fb3.index, columns=years)

#for j in years:
#    curr_year = cia_fb3.xs((str(j)), level=('Year'), axis=1)
#    for i in null_country_heatmap.index:
#        null_country_heatmap.ix[i][j] = curr_year.ix[i].isnull().sum()  