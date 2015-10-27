# SF_DAT_17_WORK
Data Science Project

October 26, 2015

Using the CIA factbook country rankings for predictive and descriptive analytics.

by Noel Carrascal

Overview

The CIA world fact-book is a description US government profiles of countries and territories around the world. 
Information on geography, people, government, transportation, economy, communications, etc. The information is 
reliable and can be used as input to do predictive and descriptive analytics. The factbook contains information 
for two hundred and sixty one countries grouped in 9 categories: Introduction, Geography, People and Society, 
Government, Economy, Energy, Communications, Transportation and Military. Countries are also divided into 13 
regions: Oceans, Africa, Antarctica, Australia-Oceania, Central America and Caribbean, Central Asia, East & 
Southeast Asia, Europe, Middle East, North America, South America, South Asia and Ocean. Countries are ranked 
by 76 fields such as Surface Area, population, GDP, birth rate, etc. 

For this project I will start with the 2014 factbook to predict GDP (gross domestic product purchasing power). 
The 2014 factbook has GDP information for the previous three years. I will use those numbers to predict GDP for 
2014 for every country. This is because the 2014 factbook was published in the middle of the year and do not 
include values for that same year. An interesting part of this project is that GDP is predicted for each country
using a four data points, but it is done for every country; That is, a few data points for many variables instead
of lots of data points for a few variables. 

I will use regression analysis and other algorithms to predict GDP and rankings. I will use correlation
analysis to relate rankings from different fields and reveal which ones are more closely related to GDP.
These field correlations could then be used to improve predictions obtained from regression analysis of GDP alone. 
I believe I can finish this by the end of the class. The following analysis will be done if time permits. 

-Comparison of clustering methods using country rankings of some the 76 fields, can we group countries in novel,
more descriptive ways?
-The 76 fields can be considered as multiple dimensions of each country. I want to apply principal component 
analysis to do a multivariate analysis. Which countries have the largest fluctuations in the 76 fields rankings?
-I want to try to answer the question of how much information in the CIA factbook can be used as input for the 
prediction of currency fluctuations. I could try to relate CIA factbook data with currency exchange data from 
the Federal reserve. The hypothesis is that information on some of the rankings could be an indicator of long-term 
currency fluctuations. This could be coupled with methods that predict short term, daily currency fluctuations to make
a more robust algorithm. 

Data source 
I have curated the 2014 factbook into RVs files that are found in this repository. I removed a lot of information 
to focus on parts of the fact-book that can be quantified and ranked.

Code
I have written a python program that loads and cleans the information in the csv files. For now, it just places the
ranking data in a 261 x 76 numpy array. This array will be the primary data structure to do the analysis described 
above. Not much else have been done on this project because I just figured out what to do with the data.  
