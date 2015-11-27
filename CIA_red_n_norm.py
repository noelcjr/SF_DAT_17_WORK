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

cia_fb_stats = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_fb_linear_reg_imputation.csv',index_col=[0,1], header=[0, 1, 2])
cia_fb = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_fb_linear_reg_imputation.csv',index_col=[0,1], header=[0, 1, 2])

years = [2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
catss = ['Geography','Economy','Communications','Transportation','Military','People and Society']
stats_on_field = ['nulls','a1','b1','2014','a2','b2','2013']

fields = []
for i in cia_fb.columns:
    if i[2] == '2014':
        fields.append((i[1]))
# I am changing the units for some of the fields. S
country_nulls = []
for i in cia_fb.index:
    country_nulls.append()
    