# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 11:51:35 2015

Source for CIA Factbooks:
https://www.cia.gov/library/publications/download/

I downloaded all rankorder.zip files going back to 2004. Factbooks before 2004
have no rankorder.zip files, so I do not consider them. As far as I look into
the files downloaded, factbooks got standardize after 2004, with a few additional
changes in 2006.

All data comes from the CIA website; however, when I started this project and
I wasn't familiar with the factbook, I downloaded a MySQL dump from:
http://jmatchparser.sourceforge.net/factbook/. 
It allowed me to explore the tables of countries, fields, categories, regions 
and rankings usin SQL. I dumped the MySQL tables from that download to CSV 
files which I then used as a Starting point for this project. Why not start 
from the CIA factbook directly? That should be the right wa to do it, and it 
should be done in the future. But becasue I have found so many problems with 
the origianl CIA files, I will not get list of countries, fields and categories 
from the  CIA for now. Using these dumped tables I look for data in the CIA
Factbook. 

This python program reads files from the CIA factbook archive. It only reads data
from ranks by 30 fields. Of all the fields considered by the CIA, only 76
are ranked, and of those only 30 fields in 2014 have been consistently maintain
from 2004 and 2014. I will only work with those fields.

I also used existing countries in 2014. Some countries have disappeard, changed
name or divided before 2014 and are not considered with the exception of two
countries. Cape Verde changed its name to Cabo Verde and I fixed that to consider
the country. Serbia and Montenegro dsplit in 2006. They are considered separatedly
here since 2006. Before that, the joined country was not considered.  

I plan to make this code more general in the future. Its current functionality 
is for the purpose of my project only.
 
@author: Noel Carrascal
@email: noelcarrascal@gmail.com
"""
import pandas as pd
import numpy as np
import os, sys
from bs4 import BeautifulSoup
import os.path
 
# Load the tables. This tables are from a different source and contain the fields
# and countries considered in 2014 only. Becasue this source did not have this
# information for year previous to 2014, I used it as a starting point to analyze,
# find and read information from previous years from the CIA factbook archive
fields = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/fields.csv')
countries = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/countries.csv')
regions = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/regions.csv')
categories = pd.read_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/categories.csv')

path = '/home/noelcjr/Projects/CIA_factbook/'
years = [2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
# I know from the CIA website that there are 76 fields that can be ranked
# in 2014. I used those fields to check if they were considered in the previous
# years. This is becase the factbook changes slightly from year to year.
# The following lines check for all fields to have files for every year
# The tables above also give me the name of the files that match a given
# field (i.e. f2001.txt is GDP (purchasing power parity)
# In the following loop I remove fields that are not present in all years
removed_fields = []
for i in years:
    for j in fields.xmlid:  # Loop for reading all field
        fname = path+str(i)+'/factbook/rankorder/'+str(j)+'.txt'
        if not os.path.isfile(fname):
            removed_fields.append(j)

# Here, new_fields are those fields in 2014 that are present in all years
# going back to 2004. Now we know that the CIA hava data for these fields for
# all years between 2004 and 2014. 
removed_fields = list(set(removed_fields))
all_fields = fields['xmlid']
new_fields = list(set(all_fields)-set(removed_fields))
# Description of some Units in the following dictionary
# I changed some units in some of the dictionary's fields becasue they were
# given as NANs, as can be  seen in the previous loop.
# HIV/AIDS - adult prevalence rate = % of adults 15-49 living with HIV/AIDS
# Infant mortality rate = % dead infants under 1 yr/old per 1000 live births 
#                         This needs to be fixed to percentages not per thousands
# Birth Rate = % Births per year per 1000 persons in population. Fix from thousands to %
# Death Rate = % Births per year per 1000 persons in population. Fix from thousands to %
# Unemployment Rate = % of labor force unemployed
# Military expenditures, Public debt = % of GDP',
# Total fertility rate = children born/woman. Change to percentage of population
# NANs = HIV/AIDS - deaths, HIV/AIDS - people living with HIV/AIDS, Internet users
#        Telephones - mobile cellular, Telephones - main lines in use, Exports
#        Debt - external, Labor force, Population, Internet hosts, 
#        Reserves of foreign exchange and gold
field_units = {'HIV/AIDS - deaths':'humans', \
'HIV/AIDS - people living with HIV/AIDS':'humans', \
'HIV/AIDS - adult prevalence rate':'%', \
'Internet users':'humans', \
'Telephones - mobile cellular':'connections', \
'Telephones - main lines in use':'connections', \
'Exports':'dollars', \
'Debt - external':'dollars', \
'Labor force':'humans', \
'Inflation rate (consumer prices)':'%', \
'Infant mortality rate':'%', \
'Military expenditures':'%', \
'Population':'humans', \
'Birth rate':'%', \
'Internet hosts':'connections', \
'Public debt':'%', \
'Current account balance':'dollars', \
'Reserves of foreign exchange and gold':'dollars', \
'Death rate':'%', \
'Industrial production growth rate':'%', \
'Area':'kms*kms', \
'Roadways':'kms', \
'Imports':'dollars', \
'GDP - per capita (PPP)':'dollars', \
'GDP (purchasing power parity)':'dollars', \
'GDP - real growth rate':'%', \
'Railways':'kms', \
'Life expectancy at birth':'years', \
'Unemployment rate':'%', \
'Total fertility rate':'children born/woman'}
# The following loop joins file names for the field  xmlid,
# Category, field, units curated, and units from CIA Factbook in field_tuples.
field_tuples = []
for i in new_fields:
    catid = int(fields.categoryid[fields.xmlid == i])
    cat = str(categories['name'][categories.id == catid]).split('\n')[0].split()
    fld = str(fields.name[(fields.categoryid == catid) & (fields.xmlid == i)]).split('\n')[0].split()
    b = str(fields.unit[fields.xmlid == i]).split('\n')[0]
    b = b.split()[1:len(b)]
    field_tuples.append((i,' '.join(cat[1:len(cat)]),' '.join(fld[1:len(fld)]),field_units[' '.join(fld[1:len(fld)])],' '.join(b)))

columns2D = []
category_dict = {}
for i in field_tuples:
    a = i[2] + ' ('+i[3]+')'
    category_dict[a] = i[1]
    for j in years:
        columns2D.append((i[1], a, j))

# Sort column tuples by Categories in place
columns2D.sort(key=lambda tup: tup[0])

# Here I associate countries with regions for the DataFrame index
index = []
for i in countries['name']:
    reg = int(str(countries.regionid[countries.name == i]).split('\n')[0].split()[1])
    reg = str(regions.name[regions.id == reg]).split('\n')[0].split()
    reg = ' '.join(reg[1:len(reg)])
    index.append((i,reg))

# I now create a Data Frame to which I plan to read all new_fields from
# the CIA factbook archive. The country name is the index and the coulumn
#columns = []
#new_fields_cols = []
#fields_with_dollar_signs = []
#region = []
#for j in range(0,len(new_fields)):
#    x = str(fields[fields.xmlid == new_fields[j]]['name']).split('\n')[0].split()
#    x = ' '.join(x[1:len(x)])  # gets rid of first element
#    columns.append(x)
#columns2D = []
#categoryDict = {}
#for i in columns:
#    a = (str(categories.name[categories.id == int(fields.categoryid[fields.name == i])]).split('\n')[0]).split()
#    b = ' '.join(a[1:len(a)])
#    categoryDict[i] = b
#    for j in years:
#        columns2D.append((i,b,j))

cia_fact_book_table = pd.DataFrame(index=index, columns=columns2D)
# Create a list of list with country names
# For every country, count how many words makeup the name,
# Create columns in the array with first word of a country and number of words in the name
# Use those columns to avoid problems in the formating of files, specially before 2008.
c_list = {}
r_list = {}
for i in range(0,len(cia_fact_book_table.index)):
    temp = cia_fact_book_table.index[i][0]
    count = len(temp.split())
    c_list[temp] = count
    r_list[temp] = cia_fact_book_table.index[i][1]
# before 2012 and before Cabo Verde was called Cape Verde: FIX!!!
# Howland Island did not exist before 2012
for i in range(0,len(years)):
    count = 1
    for j in field_tuples:
        lines = [line.split() for line in open(path+'/'+str(years[i])+'/factbook/rankorder/'+j[0]+'.txt', 'r')]
        for k in lines:
            if '$' in k:
                k.remove('$')
            tempStr = k[1:len(k)]        
            for l in range(len(tempStr),0,-1):
                if (' '.join(tempStr[0:l])) in c_list:
                    country = ' '.join(tempStr[0:l])
                    if country == 'Cape Verde':
                        country = 'Cabo Verde'                    
                    # If it can't convert from string to float, it means that the there is a
                    # country that changed name in years other than 2014. This happend to
                    #  1) United States Pacific Island Wildlife Refuge. For reasons I could not explain,
                    #     but this country was eventually removed.
                    #  2) Neatherland Antilles ceased to exist or changed name in 2010.
                    #  3) Serbia and Montenegro ceased to exist by splitting into two countries in 2006.
                    # CHECK HOW TO ADDRESS THESE CASES!!!
                    try:
                        value = float(tempStr[l].replace(',',''))
                        count = count + 1
                        fld = j[2] + ' (' + j[3] + ')'
                        cat = category_dict[fld]
                        cia_fact_book_table[(cat,fld,years[i])][(country,r_list[country])] = value                      
                    except ValueError,e:
                        print "error",e,"line=",k," year",years[i]," field=",j," value=",tempStr[l]

cia_fact_book_table.columns=pd.MultiIndex.from_tuples(columns2D, names=['Category','Field','Year'])
cia_fact_book_table.index = pd.MultiIndex.from_tuples(index, names=['Country','Region'])

cia_fact_book_table.to_csv('/home/noelcjr/github/SF_DAT_17_WORK/data/cia_factbook_table.csv')


  