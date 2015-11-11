# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:24:45 2015

@author: noelcjr
"""



null_country_heatmap = []
null_country_heatmap = pd.DataFrame(index=cia_fb3.index, columns=years)

for j in years:
    curr_year = cia_fb3.xs((str(j)), level=('Year'), axis=1)
    for i in null_country_heatmap.index:
        null_country_heatmap.ix[i][j] = curr_year.ix[i].isnull().sum()  