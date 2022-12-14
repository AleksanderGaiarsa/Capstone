# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 00:32:06 2022

@author: nguye
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# Import dataframes

dtypes1 = {'Time': 'category',
           'Bullet Speed': 'float64',
         'GSR': 'float64'}

dtypes2 = {'Time': 'category',
           'Heart Rate': 'int64'}

df1 = pd.read_csv('Data0.csv',
    dtype = dtypes1,
    usecols = list(dtypes1))

df1 = df1.dropna()
print(df1)
df1 = df1.groupby(['Time'], as_index=False).mean('Heart Rate','GSR')
df1 = df1.dropna() # solution to add this row? check if valid
print(df1)
##### SOME ERROR HERE, WHY NA STILL PRESENT, time column is weird

df2 = pd.read_csv('HR0.csv',
    dtype = dtypes2,
    usecols = list(dtypes2))

df = pd.merge(df1,
                      df2,
                      on = 'Time',
                      how = 'inner')
df

print(df)

hr_rest = df.loc[(df['Bullet Speed'] == 10)]
hr_rest = hr_rest["Heart Rate"].mean()
print('The resting heart rate is ' + str(round(hr_rest,2)))


# TRYING WITH LINEAR AND LOGISTIC REGRESSION FIRST

# Import peak detection algorithm here #

X = df[['GSR','Heart Rate']].values
y = df['Bullet Speed'].values

model = LinearRegression()
model.fit(X, y)
print(model.coef_, model.intercept_)

# Make predictions with this model
# print(model.predict(X[:5]))

# Score the model
y_pred = model.predict(X)
y == y_pred
# print((y == y_pred).sum()) / y.shape[0] # to test how many right (%)
print("Accurary with linear regression: " + str(round(model.score(X,y),2))) # simpler way to do it

# With training and testing set split
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=101)
model.fit(X_train, y_train)
model.score(X_test, y_test) # calculate accuracy
print("Accuracy with linear regression (split): " + str(round(model.score(X_test, y_test),2)))

# print("Size of X_test: " + str(X_test.shape))
# print("Size of y_test: " + str(y_test.shape))
# print("Size of X_train: " + str(X_train.shape))
# print("Size of y_train: " + str(y_train.shape))

# Plot outputs
# X_test = X_test[:,0]
# plt.scatter(X_test, y_test, color="black")
# plt.plot(X_test, y_train, color="red", linewidth=3)
# plt.xticks(())
# plt.yticks(())
# plt.show()

#### Random Forests
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
rf.score(X_test, y_test) # calculate accuracy
print("Accuracy with random forests: " + str(round(rf.score(X_test, y_test),2)))

# Tuning a random forest
param_grid = {
    'n_estimators': range(15), # Try different values
}
gs = GridSearchCV(rf, param_grid, cv = 5) # cv=5 so 5-fold cross validation
gs.fit(X,y)
print("Best parameters:", gs.best_params_) # number of estimators/trees
best_estimator = gs.best_params_.get('n_estimators')

# Elbow Graph (number of trees before reaching plateau)
n_estimators = list(range(1,101)) # try 1 to 100 trees
param_grid = {'n_estimators':n_estimators}
gs = GridSearchCV(rf, param_grid,cv = 5)
gs.fit(X,y)
scores = gs.cv_results_['mean_test_score']

# Now we want to use matplotlib to graph

plt.plot(n_estimators,scores)
plt.xlabel("n_estimators")
plt.ylabel("accuracy")
plt.xlim(0,50)
plt.ylim(0.50,0.85)
plt.show

# After plot, pick best number of trees (n_estimators)
rf = RandomForestClassifier(n_estimators = best_estimator) # put best one here
rf.fit(X_train, y_train)
rf.score(X_test, y_test) # calculate accuracy
print("New accuracy with random forests: " + str(round(rf.score(X_test, y_test),2)))

