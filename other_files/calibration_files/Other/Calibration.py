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
from sklearn.metrics import mean_squared_error, r2_score
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
    min_gsr = str(round(min(df[profile]['GSR']),2))
    max_gsr = str(round(max(df[profile]['GSR']),2))
    print('The minimum and maximum GSR of this profile is ' + min_gsr + 'and ' + max_gsr)

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

rf = RandomForestClassifier() # MAKE SPECIFIC, I did
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

rf.fit(X_train, y_train) # returns fitted random forests

lr = LinearRegression()
lr_hr = LinearRegression()
score_lr = {}
score_lr_hr = {}

# Where is X_test, y_test below

for profile in profiles:
    X_train = df[profile][['GSR']].values
    y_train = df[profile]['Bullet Speed'].values
    y_train_hr = df[profile]['Heart Rate'].values
    lr.fit(X_train, y_train)
    lr_hr.fit(X_train,y_train_hr)
    y_pred = lr.predict(X_train)
    y_pred_hr = lr_hr.predict(X_train)
    y_train == y_pred
    y_train_hr == y_pred_hr
    score_lr[profile] = str(round(r2_score(y_train, y_pred),2)) # calculate accuracy
    score_lr_hr[profile] = str(round(r2_score(y_train_hr, y_pred_hr),2))
    print("Accuracy with linear regression for profile #" + str(profile) + ": " + score_lr[profile])
    print("Accuracy HR with linear regression for profile #" + str(profile) + ": " + score_lr_hr[profile])

best_profile_index = max(score_lr, key=score_lr.get)
X_train = df[best_profile_index][['GSR']].values
y_train = df[best_profile_index]['Bullet Speed'].values
print("The best profile is profile #" + str(best_profile_index) + " with accuracy of " + score_lr[best_profile_index])

lr.fit(X_train,y_train)

##################### END OF CALIBRATION ####################

# Make predictions of bullet speed using GSR with this model
dtypes_game = {'Time': 'category',
               'Bullet Speed': 'float64',
          'GSR': 'float64'}
# Import real time data to predict:
# Note that the csv below should be the real-time game round data
df_game = pd.read_csv('Data0.csv',
    dtype = dtypes_game,
    usecols = list(dtypes_game))

df_game = df_game.dropna()
df_game = df_game.sort_values(by = 'GSR')
df_game = df_game.reset_index(drop=True)
#print(df_game)

bullet_speed_pred_rf = rf.predict(df_game[['GSR']])
bullet_speed_pred_lr = lr.predict(df_game[['GSR']])
#plt.plot(df_game[['Bullet Speed']],linewidth=0.25)
plt.scatter(df_game.index, df_game[['Bullet Speed']], s=0.1, color='black')
plt.plot(bullet_speed_pred_rf, linewidth=3)
plt.plot(bullet_speed_pred_lr, linewidth=3)
plt.legend(['Real','Random Forests (Pred)','Linear Regression (Pred)'])
plt.ylim([0,50])
plt.xlim([9000,40000])
plt.title("Stress Versus GSR")
plt.ylabel("Predicted Bullet Speed (Stress Level)")
plt.xlabel("GSR in chronological order")
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

print(df_game)

# print(bullet_speed_pred_rf)
# print(bullet_speed_pred_lr)
#print(lr.coef_, lr.intercept_)

# Make predictions of heart rate using GSR with this model
hr_pred = lr_hr.predict([[200]])
print(hr_pred)

# Define outputs
# Initialisations

# PWM = 0
# TENS = 0
# Volume = 0

# while True:
#     if (bullet_speed_pred_lr < 0):
#         PWM = 0
#         TENS = 0
#         Volume = 10
#     elif (bullet_speed_pred_lr > 50):
#         PWM = 255
#         TENS = 1   
#         Volume = 50
#     else:
#         PWM = (bullet_speed_pred_lr / 50) *255
#         Volume = round(bullet_speed_pred_lr)
#         if (bullet_speed_pred_lr > 30):
#             TENS = 1
#         else:
#             TENS = 0 

# The rf.predict defines the stress levels