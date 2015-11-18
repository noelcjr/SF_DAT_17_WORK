# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 11:51:35 2015
This file reads files from the CIA factbook archive. It only reads data
from ranks by 30 fields. Of all the fields considered by the CIA, only 76
are ranled, and of those only 30 fields have been consistently maintain
from 2004 and 2014. I will only work with those fields.

Only countries that have no null valies in all 30 fields are considered.

The output is dumped to a csv file to be loaded again for analysis.

This file is a quick and dirty approach to getting the information
from the CIA factbook for the GA project and for that purpuse I used
fields available in 2014. I plan to make this code more general in the 
future. Its current functionality is for the purpose of my project only. 
@author: Noel Carrascal
@email: noelcarrascal@gmail.com
"""
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import os.path
 
# Load the tables. This tables are from a different source and contain the
# fields and countries considered in 2014 only. Becasue this source did not have
# this information for year previous to 2014, I used it as a starting point
# to analyze find and read information from previous year from the CIA factbook archive
fields = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/fields.csv')
countries = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/countries.csv')
regions = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/regions.csv')
categories = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/categories.csv')

path = '/home/noelcjr/Projects/CIA_factbook/'
years = [2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
start_lines = [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2]
row_offset = [1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3]
# I know from the CIA website that there are 76 fields that can be ranked
# in 2014. I used those fields to check if they were considered in the previous
# years. This is becase the factbook changes slightly from year to year.
# The following lines check for all fields to have files for every year
removed_fields = []
for i in years:
    for j in fields.xmlid:  # Loop for reading all field
        fname = path+str(i)+'/factbook/rankorder/'+str(j)+'.txt'
        if not os.path.isfile(fname):
            removed_fields.append(j)

# Here, new_fields are those fields in 2014 that are present in all years
# going back to 2004. Now we know that the CIA hava data for these fields for
# all years. 
removed_fields = list(set(removed_fields))
all_fields = fields['xmlid']
new_fields = list(set(all_fields)-set(removed_fields))
#for i in new_fields:
#    print(fields[fields.xmlid == i][['categoryid','name']])
#             Category  Name
# 3 People and Soc.
# 7 Communications.
# 5 Economy.
# 8 Transportation.
# 2 Geography.
# 9 Military Expen.
# 1) f2157           3  HIV/AIDS - deaths
# 2) f2156           3  HIV/AIDS - people living with HIV/AIDS
# 3) f2155           3  HIV/AIDS - adult prevalence rate
# 4) f2153           7  Internet users
# 5) f2151           7  Telephones - mobile cellular
# 6) f2150           7  Telephones - main lines in use
# 7) f2078           5  Exports
# 8) f2079           5  Debt - external
# 9) f2095           5  Labor force
#10) f2092           5  Inflation rate (consumer prices)
#11) f2091           3  Infant mortality rate
#12) f2034           9  Military expenditures
#13) f2119           3  Population
#14) f2054           3  Birth rate
#15) f2184           7  Internet hosts
#16) f2186           5  Public debt
#17) f2187           5  Current account balance
#18) f2188           5  Reserves of foreign exchange and gold
#19) f2066           3  Death rate
#20) f2089           5  Industrial production growth rate
#21) f2147           2  Area
#22) f2085           8  Roadways
#23) f2087           5  Imports
#24) f2004           5  GDP - per capita (PPP)
#25) f2001           5  GDP (purchasing power parity)
#26) f2003           5  GDP - real growth rate
#27) f2121           8  Railways
#28) f2102           3  Life expectancy at birth
#29) f2129           5  Unemployment rate
#30) f2127           3  Total fertility rate
    
# I now create a Data Frame to which I plan to read all new_fields from
# the CIA factbook archive. The country name is the index and the coulumn
columns = []
new_fields_cols = []
fields_with_dollar_signs = []
index = []
region = []
for j in range(0,len(new_fields)):
    x = str(fields[fields.xmlid == new_fields[j]]['name']).split('\n')[0].split()
    x = ' '.join(x[1:len(x)])  # gets rid of first element
    columns.append(x)

for i in countries['name']:
    reg = int(str(countries.regionid[countries.name == i]).split('\n')[0].split()[1])
    reg = str(regions.name[regions.id == reg]).split('\n')[0].split()
    reg = ' '.join(reg[1:len(reg)])
    index.append((i,reg))


columns2D = []
categoryTuple = []
for i in columns:
    a = (str(categories.name[categories.id == int(fields.categoryid[fields.name == i])]).split('\n')[0]).split()
    b = ' '.join(a[1:len(a)])
    categoryTuple.append(b)
    for j in years:
        columns2D.append((i,b,j))

cia_fact_book_table = pd.DataFrame(index=index, columns=columns2D)
#cia_fact_book_table.columns=pd.MultiIndex.from_tuples(columns2D)
# Create a list of list with country names
# For every country, count how many words makeup the name,
# Create columns in the array with first word of a country and number of words in the name
# Use those columns to avoid problems in the formating of files, specially before 2008.
c_list = []
for i in range(0,len(cia_fact_book_table.index)):
    c_list.append(cia_fact_book_table.index[i][0].split())

for j in c_list:
    l = len(j)
    j.insert(0,l)

# before 2012 and before Cabo Verde was called Cape Verde: FIX!!!
# Howland Island did not exist before 2012
for i in range(0, len(years)):
    for j in range(0,len(new_fields)):
        # There has to be a better way to to get cat from new_fields in fewer lines.
        cat = str(fields.categoryid[fields.xmlid == new_fields[j]]).split('\n')[0].split()
        cat = categories.name[categories.id == int(' '.join(cat[1:len(cat)]))]
        cat = ' '.join(str(cat).split('\n')[0].split()).split()
        cat = ' '.join(cat[1:len(cat)])
        lines = [line.split() for line in open(path+'/'+str(years[i])+'/factbook/rankorder/'+new_fields[j]+'.txt', 'r')]
        for k in range(0,len(lines)):
            if 'updated' not in lines[k]:  # Gets rid of last line that is not data due to weird formating before 2008 and before.
                if k >= (start_lines[i]):
                    if '$' in lines[k]:
                        lines[k].remove('$')
                    # Get first word of the country name:
                    first = lines[k][1]
                    if first == 'Cape':
                        first = 'Cabo'
                    # look for matching first words in c_list and create a list
                    # of countries that mathc the first word in c_list
                    matches = []
                    for l in c_list:
                        if first == l[1]:
                            matches.append(l)
                    # If there is only one country with a given first word only
                    # then just get the name and move on. 
                    if len(matches) == 1:                    
                        country = ' '.join(lines[k][1:(matches[0][0]+1)])
                        value = lines[k][(matches[0][0]+1)]
                        if country == 'Cape Verde':
                            country = 'Cabo Verde'
                        reg = int(str(countries.regionid[countries.name == country]).split('\n')[0].split()[1])
                        reg = str(regions.name[regions.id == reg]).split('\n')[0].split()
                        reg = ' '.join(reg[1:len(reg)])
                        cia_fact_book_table[(columns[j],cat,years[i])][(country,reg)] = str(value)
                    else:
                        for m in matches:
                            m_length = m[0]
                            m_country = ' '.join(m[1:(m_length+1)])
                            for n in range(2,len(lines[k])):
                                l_country = ' '.join(lines[k][1:n])
                                if m_country == l_country:
                                    country = m_country
                                    reg = int(str(countries.regionid[countries.name == country]).split('\n')[0].split()[1])
                                    reg = str(regions.name[regions.id == reg]).split('\n')[0].split()
                                    reg = ' '.join(reg[1:len(reg)])
                                    value = lines[k][(m_length+1)]
                                    cia_fact_book_table[(columns[j],cat,years[i])][(country,reg)] = str(value)

cia_fact_book_table.columns=pd.MultiIndex.from_tuples(columns2D, names=['Field','Category','Year'])
cia_fact_book_table.index = pd.MultiIndex.from_tuples(index, names=['Country','Region'])
#import seaborn as sns
cia_fact_book_table.to_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_factbook_table.csv')
#sns.pairplot(cia_fact_book_table, x_vars=['2014 GDP (purchasing power parity)'], y_vars='2014 GDP (purchasing power parity)')
# Create a data frame with same indexes as cia_fact_book_table and with a Nans count.
#col_nulls = pd.DataFrame(index=index, columns=['Nans'])
#for i in cia_fact_book_table.index:
#    col_nulls.ix[i]['Nans'] = cia_fact_book_table[cia_fact_book_table.index == i].isnull().sum()[0:330].sum()

# Rank countries by number of columns with null values

  