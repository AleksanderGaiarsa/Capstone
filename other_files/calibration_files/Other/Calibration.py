# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:55:40 2022

@author: nguye
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Import dataframes
dtypes1 = {'Time': 'category',
           'Bullet Speed': 'float64',
         'GSR': 'float64'}

dtypes2 = {'Time': 'category',
           'Heart Rate': 'int64'}

profiles = range(3)
df1 = {}
df2 = {}
df = {}
hr_rest = {}

for profile in profiles:

    df1[profile] = pd.read_csv('Data' + str(profile) + '.csv',
    dtype = dtypes1,
    usecols = list(dtypes1))
    
    df1[profile] = df1[profile].dropna(thresh=3)
    df1[profile] = df1[profile].groupby(['Time'], as_index=False).mean('Heart Rate','GSR')
    df1[profile] = df1[profile].dropna()
    print(df1[profile])
    
    df2[profile] = pd.read_csv('HR' + str(profile) + '.csv',
    dtype = dtypes2,
    usecols = list(dtypes2))
    
    df[profile] = pd.merge(df1[profile],
                      df2[profile],
                      on = 'Time',
                      how = 'inner')
    df[profile]
    
    hr_rest[profile] = df[profile].loc[(df[profile]['Bullet Speed'] == 10)]
    hr_rest[profile] = hr_rest[profile]["Heart Rate"].mean()
    print('The resting heart rate of profile #' + str(profile) + ' is ' + str(round(hr_rest[profile],2)))

# GATHER CALIBRATION ROUND DATA
# Aleks would save down the gsr + speed data gathered during 30-second calibration
# and save it as 'Calibration'(change line below to Calibration)

df_calib = pd.read_csv('Data0.csv',
    dtype = dtypes1,
    usecols = list(dtypes1))

df_calib = df_calib.dropna(thresh=3)
df_calib = df_calib.groupby(['Time'], as_index=False).mean('GSR')
df_calib = df_calib.dropna()

# Compare with test data

X_test = df_calib[['GSR']].values
y_test = df_calib['Bullet Speed'].values

# Set X_train, y_train for all the profiles

rf = RandomForestClassifier() # MAKE SPECIFIC
score_rf = {}

for profile in profiles:
    X_train = df[profile][['GSR']].values
    y_train = df[profile]['Bullet Speed'].values
    rf.fit(X_train, y_train)
    score_rf[profile] = str(round(rf.score(X_test, y_test),2)) # calculate accuracy
    print("Accuracy with random forests for profile #" + str(profile) + ": " + score_rf[profile])

best_profile_index = max(score_rf, key=score_rf.get)
X_train = df[best_profile_index][['GSR']].values
y_train = df[best_profile_index]['Bullet Speed'].values
print("The best profile is profile #" + str(best_profile_index) + " with accuracy of " + score_rf[best_profile_index])

lr = LinearRegression()
score_lr = {}

for profile in profiles:
    X_train = df[profile][['GSR']].values
    y_train = df[profile]['Bullet Speed'].values
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    y_train == y_pred
    score_lr[profile] = str(round(mean_squared_error(y_train, y_pred),2)) # calculate accuracy
    print("Accuracy with linear regression for profile #" + str(profile) + ": " + score_lr[profile])

best_profile_index = max(score_lr, key=score_lr.get)
X_train = df[best_profile_index][['GSR']].values
y_train = df[best_profile_index]['Bullet Speed'].values
print("The best profile is profile #" + str(best_profile_index) + " with accuracy of " + score_lr[best_profile_index])

rf.fit(X_train, y_train) # returns fitted random forests

##################### END OF CALIBRATION ####################

# # Make predictions with this model
# dtypes_game = {'Time': 'category',
#           'GSR': 'float64'}
# # Import real time data to predict:

# df_game = pd.read_csv('Data0.csv',
#     dtype = dtypes_game,
#     usecols = list(dtypes_game))

# bullet_speed_pred = rf.predict([[200]]) 

# #print(bullet_speed_pred)
    
    
    
#print(rf.predict(df_game[['GSR']].values))