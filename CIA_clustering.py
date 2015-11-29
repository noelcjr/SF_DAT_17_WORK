# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 14:53:57 2015

@author: noelc
"""
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics

cia_fb77_stats = pd.read_csv('C:\\Users\\noelc\\OneDrive\\Documents\\GitHub\\SF_DAT_17_WORK\\data\\cia_fb_77_linear_reg_coef.csv',index_col=[0,1], header=[0, 1, 2])
cia_fb77 = pd.read_csv('C:\\Users\\noelc\\OneDrive\\Documents\\GitHub\\SF_DAT_17_WORK\\data\\cia_fb_77_reduction_n_normalization.csv',index_col=[0,1], header=[0, 1, 2])

years = [2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
catss = ['Geography','Economy','Communications','Transportation','Military','People and Society']
stats_on_field = ['nulls','a1','b1','2014','a2','b2','2013']

fields = []
fields2 = []
for i in cia_fb77.columns:
    if i[2] == '2014':
        fields.append((i[0],i[1]))
        fields2.append((i[0],i[1][0:(i[1].find('(')-1)]))

indx = []
for i in cia_fb77.index:
    if i[1] == 'Central America and Caribbean':
        if i[0] == 'Dominican Republic':
            indx.append(('Dom. Rep.','Central America & Carib'))
        else:
            indx.append((i[0],'Central America & Carib'))
    elif i[1] == 'East &amp; Southeast Asia':
        indx.append((i[0],'East & S.E Asia'))
    else:
        indx.append((i[0],i[1]))
        
      
for i in cia_fb77.columns:
    temp = cia_fb77.xs((i[0],i[1]), level=('Category','Field'), axis=1)

cia_fb77_mean = pd.DataFrame(cia_fb77, index=cia_fb77.index, columns=fields)  
cia_fb77_mean.columns=pd.MultiIndex.from_tuples(cia_fb77_mean.columns, names=['Category','Field'])
cia_fb77_mean.index=pd.MultiIndex.from_tuples(cia_fb77_mean.index, names=['Country','Region',])
count = 0
for i in cia_fb77.columns:
    temp = cia_fb77.xs((i[0],i[1]), level=('Category','Field'), axis=1)
    for j in temp.index:
        cia_fb77_mean.loc[j,(i[0],i[1])] = cia_fb77.loc[j,(i[0],i[1])].sum()/len(cia_fb77.loc[j,(i[0],i[1])])

cia_fb77_mean.columns = fields2
cia_fb77_mean.index = indx
a4_dims = (18, 8)
fig, ax = plt.subplots(figsize=a4_dims)
sns.heatmap(data=cia_fb77_mean.T, ax=ax)
cia_fb77_mean.columns = fields
cia_fb77_mean.columns=pd.MultiIndex.from_tuples(cia_fb77_mean.columns, names=['Category','Field'])
cia_fb77_mean.index=pd.MultiIndex.from_tuples(cia_fb77_mean.index, names=['Country','Region',])

X = cia_fb77_mean.values

np.random.seed(0)

k_rng = range(1,35)
est = [KMeans(n_clusters = k).fit(X) for k in k_rng]
silhouette_score = [metrics.silhouette_score(X, e.labels_, metric='euclidean') for e in est[1:]]
plt.plot(k_rng[1:], silhouette_score, 'b*-')
plt.xlim([1,35])
plt.grid(True)
plt.title('Silhouette Coefficient')

within_sum_squares = [e.inertia_ for e in est]
plt.plot(k_rng, within_sum_squares, 'b*-')
plt.xlim([1,35])
plt.grid(True)
plt.title('Within Sum of Squared Errors')

