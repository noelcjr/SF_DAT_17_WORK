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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn import tree

cia_fb77_means = pd.read_csv('/home/noel/Projects/CIA_factbook/SF_DAT_17_WORK/data/cia_fb77_means.csv',index_col=[0,1], header=[0, 1])

target = cia_fb77_means[('Economy','GDP - real growth rate (%)')]
median =  np.median(list(target))
for i in target.index:
    if target.ix[i] >= median:
        target.ix[i] = 1
    else:
        target.ix[i] = 0
## We delete the three fields directly related to GDP
del cia_fb77_means[('Economy','GDP - per capita (PPP) (dollars)')]
del cia_fb77_means[('Economy','GDP (purchasing power parity) (dollars)')]
del cia_fb77_means[('Economy','GDP - real growth rate (%)')]

X = cia_fb77_means
y = target

knn = KNeighborsClassifier(n_neighbors=5)
cross_val_score(knn, X, y, cv=10, scoring='roc_auc').mean()
#SCORE = 0.5210
knn2 = KNeighborsClassifier(n_neighbors=12)
cross_val_score(knn2, X, y, cv=10, scoring='roc_auc').mean()
#SCORE= 0.5113

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
cross_val_score(logreg, X, y, cv=10, scoring='roc_auc').mean()
#SCORE = 0.5534

# Conduct a grid search for the best tree depth
ctree = tree.DecisionTreeClassifier(random_state=1)
depth_range = range(1, 20)
param_grid = dict(max_depth=depth_range)
grid = GridSearchCV(ctree, param_grid, cv=10, scoring='roc_auc')
grid.fit(X, y)

# Check out the scores of the grid search
grid_mean_scores = [result[1] for result in grid.grid_scores_]

# Plot the results of the grid search
plt.figure()
plt.plot(depth_range, grid_mean_scores)
plt.hold(True)
plt.grid(True)
plt.plot(grid.best_params_['max_depth'], grid.best_score_, 'ro', markersize=12, markeredgewidth=1.5,
         markerfacecolor='None', markeredgecolor='r')
         
# Conduct a grid search for the best tree depth
ctree = tree.DecisionTreeClassifier(random_state=1)
depth_range = range(1, 20)
criterion_range = ['gini', 'entropy']
max_feaure_range = range(1,5)
param_grid = dict(max_depth=depth_range, criterion=criterion_range, max_features=max_feaure_range)
grid = GridSearchCV(ctree, param_grid, cv=10, scoring='roc_auc')
grid.fit(X, y)

# Check out the scores of the grid search
grid_mean_scores = [result[1] for result in grid.grid_scores_]

# Get the best estimator
best = grid.best_estimator_
# Max_dpth = 3, criterion='entropy', SCORE=0.765
best.feature_importances_
plt.figure()
#BUG: I do not rememer how to get the feture name from the feature_importances_
plt.plot(best.feature_importances_)

