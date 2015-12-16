# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 14:21:40 2015

@author: noel
"""
import pandas as pd
import numpy as np
import math
import seaborn as sns

cia_fb77_means = pd.read_csv('/home/noel/Projects/CIA_factbook/SF_DAT_17_WORK/data/cia_fb77_means.csv',index_col=[0,1], header=[0, 1])
drinks = pd.read_csv('/home/noel/Projects/CIA_factbook/SF_DAT_17_WORK/data/drinks.csv', na_filter=False)

EU = ['Austria','Belgium','Bulgaria','Cyprus','Croatia','Czech Republic', \
'Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland', \
'Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland', \
'Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','United Kingdom']

drinks_EU = 0
for i in EU:
    drinks_EU = drinks_EU + float(drinks.total_litres_of_pure_alcohol[drinks.country == i])
#Inner join of drinks and cia_fb77_means
cia_fb77_means[('People and Society','drinks')] = -1
in_countries = []
for i in cia_fb77_means.index:
    if i[0] == 'Congo, Republic of the':
        i2 = ('Congo','Africa')
    elif i[0] == 'Dom. Rep.':
        i2 = ('Dominican Republic','Central America & Carib')
    elif i[0] == 'Russia':
        i2 = ('Russian Federation','Central Asia')
    elif i[0] == 'Korea, South':
        i2 = ('South Korea','East & S.E Asia')
    elif i[0] == 'Bosnia and Herzegovina':
        i2 = ('Bosnia-Herzegovina','Europe')
    elif i[0] == 'United States':
        i2 = ('USA','North America')
    else:
        i2 = i
            
    for j in drinks.country:
        if i2[0] == j:
            cia_fb77_means.loc[i,('People and Society','drinks')] = float(drinks.total_litres_of_pure_alcohol[drinks.country == j])
    
cia_fb77_means.loc[('European Union', 'Europe'),('People and Society','drinks')] = drinks_EU
#Check for values that were not assigned in the previous loop
# if nothing prints, column for drinks is complete. 
for i in cia_fb77_means.index:
    if cia_fb77_means.loc[i,('People and Society','drinks')] == -1:
        print(i,cia_fb77_means.loc[i,('People and Society','drinks')])

cia_fb77_means[('People and Society','drinks')] = (cia_fb77_means[('People and Society','drinks')]-cia_fb77_means[('People and Society','drinks')].min())/(cia_fb77_means[('People and Society','drinks')].max()-cia_fb77_means[('People and Society','drinks')].min())
cia_fb77_means[('People and Society','drinks')] = cia_fb77_means[('People and Society','drinks')]/cia_fb77_means[('People and Society','drinks')].sum()

cia_fb77_means.corr()

# display correlation matrix in Seaborn using a heatmap
sns.heatmap(cia_fb77_means.corr())


        