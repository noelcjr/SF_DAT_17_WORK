# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:24:45 2015
@author: noelcjr
"""
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
# We read the data frame obtained from the output of cia_get_data.py
cia_fb = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_factbook_table.csv',index_col=[0,1], header=[0, 1, 2])
years = [2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
catss = ['Geography','Economy','Communications','Transportation','Military','People and Society']
new_tuples_cols = []
stats_on_field = ['nulls','a1','b1','2014','a2','b2','2013']
# Here I generate some lists that are used in multindexing
list_2014 = []
list_2014_2013 = []
for i in cia_fb.columns:
    if i[2] == '2014':
        list_2014.append((i[0],i[1],'2014'))
        list_2014_2013.append((i[0],i[1],'2014'))
        list_2014_2013.append((i[0],i[1],'2013'))
        for j in stats_on_field:
            new_tuples_cols.append((i[0],i[1],j))

new_tuples_index = []
for i in cia_fb.index:
    new_tuples_index.append((i[0],i[1]))
# With some of the Tuples generated for multiindexing I generate a DataFrame
countries_lr_stats = pd.DataFrame(index=cia_fb.index, columns=new_tuples_cols)  
countries_lr_stats.columns=pd.MultiIndex.from_tuples(new_tuples_cols, names=['Category','Field','Stats'])
# The following line flatens a multi index dataframe
# testPDF.columns = [' @ '.join(col).strip() for col in testPDF.columns.values]
cia_fb_2014Bool = pd.DataFrame(index=cia_fb.index,columns=list_2014)
for i in cia_fb.columns:
    if i[2] == '2014':
        cia_fb_2014Bool.loc[:][(i[1],i[0],'2014')] = cia_fb.xs((i[0],i[1],'2014'), level=('Category','Field','Year'), axis=1).isnull()
# Before doing linear regressions, create a boolean dataframe for 2014 only that
# records if a field/category it is null before imputing a value on it.
# This would answer how good is linear regresion in predicting a Field when the value
# is known and using the regression with all points and with points up to 2013!!!
supercount = 0
for i in cia_fb.columns:
    temp = cia_fb.xs((i[0],i[1]), level=('Category','Field'), axis=1)
    for j in temp.index:
        c = pd.DataFrame(temp.loc[j[0],j[1]])
        c.columns = ['value']    # Changes the complex column  name to just values
        nulls = c['value'].isnull().sum()
        nulls2 =  c['value'][1:len(c)].isnull().sum()
        #Keep track, then eliminate nulls before linear regression
        #After regression use cnull to predict values for missing data.
        countries_lr_stats.loc[(j[0],j[1]),(i[0],i[1],'nulls')] = int(nulls)
        cnull = c.isnull()
        cnull['year'] = cnull.index
        c.dropna(inplace=True)
        if nulls < 10:
            c['year'] = c.index
            # Fix types to be able to do linear regression. Some values are read
            # as string such as: "12,000,000" The following two lines remove
            # comas so that the string can be converted to an int or float
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
            countries_lr_stats.loc[j,(i[0],i[1],'a1')] = float(linreg.coef_)
            countries_lr_stats.loc[j,(i[0],i[1],'b1')] = float(linreg.intercept_)
            val = linreg.predict(2014)[0]
            countries_lr_stats.loc[j,(i[0],i[1],'2014')] = float(val)
            #With All null values eliminated and linear regressions calculated... move on to fill in missing values in original
            #cia factbook data.
            count = 0
            for k in cnull['value']:
                if k:
                    cia_fb.loc[j,(i[0],i[1],cnull.year[str(years[count])])] = float(linreg.predict(years[count])[0]) 
                    #print('Null:',temp.index[j],years[count])
                    supercount = supercount + 1
                count = count + 1
            if nulls2 < 9:  # This means that 2014 is not null and we can do the linear regression upto 2013, and estimate 2014
                linreg2 = LinearRegression()
                linreg2.fit(X[1:len(X)],y[1:len(y)])
                countries_lr_stats.loc[j,(i[0],i[1],'a2')] = float(linreg2.coef_)
                countries_lr_stats.loc[j,(i[0],i[1],'b2')] = float(linreg2.intercept_)
                val2 = linreg2.predict(2014)[0]
                countries_lr_stats.loc[j,(i[0],i[1],'2013')] = float(val2)

cia_fb.isnull().sum().sum()
# 16719
# Even after imputation, the European Union have null values which I impute from 
# the sum, or average, of the values of the  countries that form th EU.
EU = ['Austria','Belgium','Bulgaria','Cyprus','Croatia','Czech Republic', \
'Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland', \
'Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland', \
'Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','United Kingdom']

count = 0
for i in cia_fb.columns:
        if np.isnan(cia_fb.loc[('European Union', 'Europe'),(i[0],i[1],i[2])]):
            print('EU:',i[0],i[1],i[2],cia_fb.loc[('European Union', 'Europe'),(i[0],i[1],i[2])])
            count = 0
            one_null = False
            for j in EU:
                if np.isnan(cia_fb.loc[(j, 'Europe'),(i[0],i[1],i[2])]):
                    # Cyprus is the only country with an nan in EU for HIV deaths. I will assume
                    # This number is 0 so that EU has a complete set of data. I will not make this
                    # assumptions for other countries.
                    if j == 'Cyprus':
                        if i[1] == 'HIV/AIDS - deaths (humans)':
                            cia_fb.loc[(j, 'Europe'),(i[0],i[1],i[2])] = 0
                        else:
                            one_null = True
                    else:
                        one_null = True
                else:
                    if i[1] == 'HIV/AIDS - deaths (humans)':
                        count = count + cia_fb.loc[(j, 'Europe'),(i[0],i[1],i[2])]
                    elif i[1] == 'HIV/AIDS - people living with HIV/AIDS (humans)':
                        count = count + cia_fb.loc[(j, 'Europe'),(i[0],i[1],i[2])]
                    elif i[1] == 'HIV/AIDS - adult prevalence rate (%)':
                        count = count + cia_fb.loc[(j, 'Europe'),(i[0],i[1],i[2])]/len(EU)
                    elif i[1] == 'Military expenditures (%)':
                        count = count + cia_fb.loc[(j, 'Europe'),(i[0],i[1],i[2])]/len(EU)
                        print('Military Expend:',count)
                    elif i[1] == 'Public debt (%)':
                        count = count + cia_fb.loc[(j, 'Europe'),(i[0],i[1],i[2])]/len(EU)
            if not one_null:
                cia_fb.loc[('European Union', 'Europe'),(i[0],i[1],i[2])] = count
                        
#CHECK previous loop logic with military espenditures
#tup = ('Military','Military expenditures (%)','2004')
#tup = ('Transportation','Railways (kms)','2004')
#cia_fb.loc[('European Union', 'Europe'),tup]
#count  = 0
#for i in EU:    
#    count = count + cia_fb.loc[(i, 'Europe'),tup]
#    print(i,cia_fb.loc[(i, 'Europe'),tup],count)

# Malta Rail way history: https://en.wikipedia.org/wiki/Malta_Railway
# It is safe to impute 0 to all nans for railways. 
# For cyprus: cia_fb.loc[('Malta', 'Europe'),('Transportation','Railways (kms)',str(y))] = 0
# for Industrial production Malta field, an rough assumption of 0 was made.
# This imputations are not based on statistics but because they are part of the EU,
# an exception was made. The assumption are not believed to play a big role in statistics
# because this countries are small compare to the size of the EU
for y in years:
    cia_fb.loc[('Malta', 'Europe'),('Transportation','Railways (kms)',str(y))] = 0
    cia_fb.loc[('Cyprus', 'Europe'),('Transportation','Railways (kms)',str(y))] = 0
    if y != 2014:
        cia_fb.loc[('Malta', 'Europe'),('Economy','Industrial production growth rate (%)',str(y))] = 0
    

cia_fb.isnull().sum().sum()
# 16622= 16719 - 54(EU imputes linear regression) - 11(Cyprus HIV/AIDS - deaths) - 11(Malta Railways) -
# 10 (Malta Indust Product) - 11 (cyprus railways)
#################################################################################################
#################################################################################################
values = []
# We bild a dataframe with the values for 2014 and the prediction for 2014 from data up to 2013
# (labeledcolumsn 2014 and 2013).
comp_14_13_lm = pd.DataFrame(index=cia_fb.index,columns=list_2014_2013)
comp_14_13_lm.columns=pd.MultiIndex.from_tuples(list_2014_2013, names=['Category','Field','Year'])
for h in new_tuples_index:
    for i in list_2014:
        if (not np.isnan(cia_fb.loc[h,i])) & (not np.isnan(countries_lr_stats.ix[h,(i[0],i[1],'2013')])):
            comp_14_13_lm.loc[h,(i[0],i[1],'2013')] = countries_lr_stats.ix[h,(i[0],i[1],'2013')]
            comp_14_13_lm.loc[h,(i[0],i[1],'2014')] = cia_fb.loc[h,i]

#For the box plot I need to normaliza and World and European Union are sums
#of countries already in the dataframe, so they need to go
droplist = [('World','Oceans'),('European Union','Europe')]
comp_14_13_lm.drop(droplist,inplace=True)

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

rmse_mean = []
rmse_std = []
rmse_labels = []
rmse_colors = []
#ax.set_xticklabels(['Sample1', 'Sample2', 'Sample3', 'Sample4'])
for i in list_2014:
    # COMENT THE NEXT TWO LINES IF TESTING/DEBUGGING THIS LOOP 
    if i == ('Economy','Inflation rate (consumer prices) (%)','2014'):
        comp_14_13_lm.drop([('Zimbabwe','Africa')],inplace=True)
    x = comp_14_13_lm.loc[:,(i[0],i[1],'2014')]
    y = comp_14_13_lm.loc[:,(i[0],i[1],'2013')]
    x.dropna(inplace=True)
    y.dropna(inplace=True)
    x.astype(float)
    y.astype(float)
    x = x.values
    y = y.values
    x=x.astype(float)
    y=y.astype(float)
    # NC is the normalization constant to make results comparable across fields
    NC = x.sum()
    x = x/NC
    y = y/NC
    # y= prediction, x=targets
    rmse_mean.append(np.sqrt(((y - x) ** 2).mean()))
    rmse_std.append(np.sqrt(((y - x) ** 2).std()))
    rmse_labels.append(str(i[1]+'-'+i[0]))
    
for jj in list_2014:
    if jj[0] == 'Communications':
        rmse_colors.append('r')
    elif jj[0] == 'Economy':
        rmse_colors.append('b')
    elif jj[0] == 'Geography':
        rmse_colors.append('y')
    elif jj[0] == 'Military':
        rmse_colors.append('m')
    elif jj[0] == 'People and Society':
        rmse_colors.append('g')
    elif jj[0] == 'Transportation':
        rmse_colors.append('k')
        
y_pos = np.arange(len(rmse_mean))
error = np.array(rmse_std)

barh_list = plt.barh(y_pos, np.array(rmse_mean), align='center', alpha=0.4)
for jj in range(0,len(rmse_colors)):
    barh_list[jj].set_color(rmse_colors[jj])
plt.yticks(y_pos, tuple(rmse_labels))
plt.xlabel('%')
plt.title('RMSE for fields')
plt.show()
#for hh in range(0,len(x.index)):
#    print(str.format('{0:.2f}',x.ix[hh]['14']),str.format('{0:.2f}',x.ix[hh]['13']),str.format('{0:.2f}',x.ix[hh]['12']),str.format('{0:.2f}',x.ix[hh]['11']),str.format('{0:.2f}',x.ix[hh]['10']),str.format('{0:.2f}',x.ix[hh]['9']),str.format('{0:.2f}',x.ix[hh]['8']),str.format('{0:.2f}',x.ix[hh]['7']),str.format('{0:.2f}',x.ix[hh]['6']),str.format('{0:.2f}',x.ix[hh]['5']),str.format('{0:.2f}',x.ix[hh]['4'])
# NULLS by country
# Get rid of Oceans, Poles, World, territories, and Fill Up European Union from countries
# Create heat map with nullvalues per fields. After I regularize the data, I could discard
# some fields with redundant or many null Values.
country_null = []
for i in cia_fb.index:
    country_null.append((i[0],i[1],cia_fb.loc[i[0]].isnull().sum().sum()))

#NULSS by field
count = 0
for i in list_2014:
     count = count + cia_fb.xs((i[1]), level=('Field'), axis=1).isnull().sum().sum()
     print(i[1],cia_fb.xs((i[1]), level=('Field'), axis=1).isnull().sum().sum(),count) 

#NULLS by category
for i in catss:
    temp = cia_fb.xs((i), level=('Category'), axis=1)   # Change cia_fb to cia_200fb
    print(i,temp.isnull().sum().sum())

list_tuples = []
for i in list_2014:
    list_tuples.append((i[0],i[1]))
     
null_heatmap = pd.DataFrame(index=list_tuples, columns=years)
null_heatmap.index = pd.MultiIndex.from_tuples(list_tuples, names=['Category','Field'])
null_heatmap.fillna(0, inplace=True)

for i in list_2014:
    for j in years:
        null_heatmap.ix[(i[0],i[1])][j] = cia_fb.xs((i[0],i[1],str(j)), level=('Category','Field','Year'), axis=1).isnull().sum().sum()

sns.heatmap(null_heatmap)
    
countries_lr_stats.to_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_fb_linear_reg_coef.csv')
cia_fb.to_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_fb_linear_reg_imputation.csv')

