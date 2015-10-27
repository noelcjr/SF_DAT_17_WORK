"""
This file loads tables from the mini CIA factbook mysql database

This is a temporary script file.
"""
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
# Load the tables.
values = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/values.csv')
countries = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/countries.csv')
fields = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/fields.csv')
ranks = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/ranks.csv')
regions = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/regions.csv')
categories = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/categories.csv')
# Clean up the dataframes to get rid of unecessary columns
del countries['photocount']
del countries['flag']
del countries['locator']
del ranks['datetext']
del ranks['dateearliest']
del ranks['datelatest']
del ranks['dateestimated']
#replace all empty values with an empty string
values.replace(np.nan,'nan', regex=True, inplace=True)
countries.replace(np.nan,'nan', regex=True, inplace=True)
fields.replace(np.nan,'nan', regex=True, inplace=True)
# Gets rid of HTML tags in values['value']
# Takes a while to run (10 min) uncomment if needed
#
#for i in range(0,len(values)):
#    b = BeautifulSoup(values['value'][i])
#    paragraphs = b.find("body").findAll("p")
#    values['value'][i] = ""
#    for paragraph in paragraphs:
#        values['value'][i] += paragraph.text + " "
        
# Gets rid of HTML tags in categories['description']
#for i in range(0,len(categories)):
#    b = BeautifulSoup(categories['description'][i])
#    paragraphs = b.find("body").findAll("p")
#    categories['description'][i] = ""
#    for paragraph in paragraphs:
#        categories['description'][i] += paragraph.text + " "


# Generates a data frame indexed by country abreviation name.
# The columns corresponds to 76 fields and they contain
# only ranking information such as Surface Area, Population,
# Birth rate, etc. This is the data structure I want feed into
# a machine learning algorithm to predict changes in the
# 2015 rankings. 
columns = [fields['name'][i] for i in range(0,len(fields))]
index = list(countries['xmlid'])
data = np.zeros((len(index),len(columns)))

row_ranks = pd.DataFrame(data, index=index, columns=columns)

jndx = 0
for i in range(0,len(columns)):
    rank_order = 1
    country_id = ranks[ranks['fieldid'] == fields['id'][i]]['country'] ## 7 should be a varaibl
    for j in range(jndx,jndx+len(country_id)):
        row_ranks[columns[i]][country_id[j]] = rank_order
        rank_order += 1
    jndx += len(country_id)

# Ranking places countries with 0 values first. 
row_ranks.sort_index(by=['Area'])
