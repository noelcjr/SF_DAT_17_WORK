# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 22:31:17 2015

@author: noelcjr
"""
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

cia_fb_stats = pd.read_csv('C:\\Users\\noelc\\OneDrive\\Documents\\GitHub\\SF_DAT_17_WORK\\data\\cia_fb_linear_reg_imputation.csv',index_col=[0,1], header=[0, 1, 2])
cia_fb = pd.read_csv('C:\\Users\\noelc\\OneDrive\\Documents\\GitHub\\SF_DAT_17_WORK\\data\\cia_fb_linear_reg_imputation.csv',index_col=[0,1], header=[0, 1, 2])

years = [2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
catss = ['Geography','Economy','Communications','Transportation','Military','People and Society']
stats_on_field = ['nulls','a1','b1','2014','a2','b2','2013']
EU = ['Austria','Belgium','Bulgaria','Cyprus','Croatia','Czech Republic', \
'Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland', \
'Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland', \
'Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','United Kingdom']

fields = []
cols = []
for i in cia_fb.columns:
    if i[2] == '2014':
        fields.append((i[0],i[1]))

# Drop all values that have a nan. It leaves 105 countries    
cia_fb2 = cia_fb.dropna()

# I will consider the EU one country. This means that countries froming the EU
# need to be droped. This is because when we normalize, we divide the value of each
# country by the sum of the field. And if the EU and its countries are both included
# during normalization, their values would be duplicated and results would be wrong.
# the field 
cia_fb2_Wd = []
for i in cia_fb2.index:
    putin = True
    for j in EU:
        if j == i[0]:
            putin = False
    if putin:
        cia_fb2_Wd.append((i[0],i[1]))
            
cia_fb3 = pd.DataFrame(cia_fb2, index=cia_fb2_Wd, columns=cia_fb.columns)  
cia_fb3.columns=pd.MultiIndex.from_tuples(cia_fb.columns, names=['Category','Field','Year'])
cia_fb3.index=pd.MultiIndex.from_tuples(cia_fb2_Wd, names=['Country','Region',])
# This normalizes the numbers in the numbers so that all calumns are in ranges between 0 and 1
# I use unit-based normalization Z = X−min(X) / max(X)−min(X) gives numbers from 0 to 1.
# A regular normalization needs to be done on top of that. N = Z/sum(Z)
for i in fields:
    for j in years:
        cia_fb3[(i[0],i[1],str(j))] = (cia_fb3[(i[0],i[1],str(j))]-cia_fb3[(i[0],i[1],str(j))].min())/(cia_fb3[(i[0],i[1],str(j))].max()-cia_fb3[(i[0],i[1],str(j))].min())
        cia_fb3[(i[0],i[1],str(j))] = cia_fb3[(i[0],i[1],str(j))]/cia_fb3[(i[0],i[1],str(j))].sum()
# Some of the columns are positive in value but are negative concepts. For example, infaltion is a
# positive value, but the higher the infalcion the worst it is for its people. So those columns
# will be multiplied by -1
for i in fields:
    negate = False
    if i[1] == 'Debt - external (dollars)':
        negate = True
    elif i[1] == 'Inflation rate (consumer prices) (%)':
        negate = True
    elif i[1] == 'Public debt (%)':
        negate = True
    elif i[1] == 'Imports (dollars)':
        negate = True
    elif i[1] == 'Unemployment rate (%)':
        negate = True
    elif i[1] == 'Military expenditures (%)':
        negate = True
    elif i[1] == 'HIV/AIDS - deaths (humans)':
        negate = True
    elif i[1] == 'HIV/AIDS - people living with HIV/AIDS (humans)':
        negate = True
    elif i[1] == 'HIV/AIDS - adult prevalence rate (%)':
        negate = True
    elif i[1] == 'Infant mortality rate (%)':
        negate = True
    elif i[1] == 'Population (humans)':
        negate = True
    elif i[1] == 'Death rate (%)':
        negate = True
        
    if negate:
        for j in years:
            cia_fb3[(i[0],i[1],str(j))] = -1*cia_fb3[(i[0],i[1],str(j))]

cia_fb3_stats = pd.DataFrame(cia_fb_stats, index=cia_fb2_Wd, columns=cia_fb_stats.columns)  
cia_fb3_stats.columns=pd.MultiIndex.from_tuples(cia_fb_stats.columns, names=['Category','Field','Stats'])
cia_fb3_stats.index=pd.MultiIndex.from_tuples(cia_fb2_Wd, names=['Country','Region',])

cia_fb3_stats.to_csv('C:\\Users\\noelc\\OneDrive\\Documents\\GitHub\\SF_DAT_17_WORK\\data\\cia_fb_77_linear_reg_coef.csv')
cia_fb3.to_csv('C:\\Users\\noelc\\OneDrive\\Documents\\GitHub\\SF_DAT_17_WORK\\data\\cia_fb_77_reduction_n_normalization.csv')

cia_fb3_stats.to_csv('C:\\Users\\noelc\\OneDrive\\Documents\\GitHub\\SF_DAT_17_WORK\\data\\cia_fb_77_linear_reg_coef.csv')
cia_fb3.to_csv('C:\\Users\\noelc\\OneDrive\\Documents\\GitHub\\SF_DAT_17_WORK\\data\\cia_fb_77_reduction_n_normalization.csv')
