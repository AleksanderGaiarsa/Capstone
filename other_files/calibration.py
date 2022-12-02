#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:15:59 2022

@author:
"""
import random
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

class Calibration():
    def __init__(self):
        #Base Readings
        self.base_heart = self.hr_rest  # seems repetitive  
        self.base_temp = self.gsr_rest

        # self.base_heart = round(self.base_heart/30,2)    # average
        # self.base_temp = round(self.base_temp/30,2)
        self.current_heart = self.base_heart
        self.current_temp = self.base_temp
        self.step_heart = 80/self.base_heart
        self.step_temp = 500/self.base_temp
        self.prev_heart_ratio = 0
        self.heart_ratio = 0
        self.prev_temp_ratio = 0
        self.temp_ratio = 0
        
        self.dtypes1 = {'Time': 'category',
                   'Bullet Speed': 'float64',
                 'GSR': 'float64'}

        self.dtypes2 = {'Time': 'category',
                   'Heart Rate': 'int64'}
        
        self.profiles = range(3) # change this if we add more profiles
        self.df1 = {}
        self.df2 = {}
        self.df = {}
        self.hr_rest = {}  
    
    def load_profiles(self):
        for profile in self.profiles:

            self.df1[profile] = pd.read_csv('Data' + str(profile) + '.csv',
            dtype = self.dtypes1,
            usecols = list(self.dtypes1))
            
            self.df1[profile] = self.df1[profile].dropna(thresh=3)
            self.df1[profile] = self.df1[profile].groupby(['Time'], as_index=False).mean('Heart Rate','GSR')
            self.df1[profile] = self.df1[profile].dropna()
            
            self.df2[profile] = pd.read_csv('HR' + str(profile) + '.csv',
            dtype = self.dtypes2,
            usecols = list(self.dtypes2))
            
            self.df[profile] = pd.merge(self.df1[profile],
                              self.df2[profile],
                              on = 'Time',
                              how = 'inner')
            self.df[profile]
            
            # Baseline heart rate
            self.hr_rest = {}
            self.hr_rest[profile]= self.df[profile].loc[(self.df[profile]['Bullet Speed'] == 10)]
            self.hr_rest[profile]= self.hr_rest["Heart Rate"].mean()
            print('The baseline heart rate is ' + str(round(self.hr_rest[profile],2)))
            
            # Get limits of GSR for each profile (useful in picking which regression model to use later)
            # Later, during game, if GSR falls outside range of profile, use linear regression to extrapolate
            self.min_gsr = str(round(min(self.df[profile]['GSR']),2))
            self.max_gsr = str(round(max(self.df[profile]['GSR']),2))
            
            # Setup
            self.X[profile] = self.df[['GSR','Heart Rate']].values
            self.y[profile] = self.df['Bullet Speed'].values
            X_train, X_test, y_train, y_test = None # resets training/testing set
            X_train, X_test, y_train, y_test = train_test_split(self.X[profile],self.y[profile], random_state=101)
            
            # Linear Regression
            self.lr[profile] = LinearRegression()
            self.lr[profile] = None
            self.lr[profile].fit(X_train, y_train)     # Save this
            
            # Random Forests
            self.rf[profile] = RandomForestClassifier()
            self.rf[profile] = None # VERIFY THIS
            self.rf[profile].fit(X_train, y_train)
            self.rf[profile].score(X_test, y_test) # calculate accuracy

            # Tuning a random forest
            param_grid = {
                'n_estimators': range(15), 
            }
            gs = GridSearchCV(self.rf[profile], param_grid, cv = 5) # cv=5 so 5-fold cross validation
            gs.fit(self.X[profile],self.y[profile])
            print("Best parameters:", gs.best_params_) # number of estimators/trees
            
            self.best_estimator = {}
            self.best_estimator[profile] = gs.best_params_.get('n_estimators')
            self.rf[profile] = RandomForestClassifier(n_estimators = self.best_estimator[profile]) # put best one here
            self.rf[profile].fit(X_train, y_train)     # Save this
            
    def calib_data(self):  
         df_calib = pd.read_csv('Calibration.csv',
             dtype = self.dtypes1,
             usecols = list(self.dtypes1))
         df_calib = df_calib.dropna(thresh=3)
         df_calib = df_calib.groupby(['Time'], as_index=False).mean('GSR')
         df_calib = df_calib.dropna()
         
         # Save down user's GSR baseline
         self.gsr_rest = self.df_calib.loc[(self.df_calib['Bullet Speed'] == 10)]
         self.gsr_rest = self.gsr_rest["GSR"].mean()
         print('The baseline GSR is ' + str(round(self.gsr_rest,2)))
         
         # Compare with test data
    
         X_test = df_calib[['GSR']].values
         y_test_rf = df_calib['Bullet Speed'].values
         y_test_lr = df_calib['Heart Rate'].values
         
         score = {}
         self.rf_game = {}     # for stress levels and bullet speed
         self.lr_game_exception = {} # for stress levels and bullet speed when gsr outside profile range
         self.lr_game = {}     # for heart rate
         for profile in self.profiles:
             self.rf_game[profile] = RandomForestClassifier(n_estimator = self.best_estimator[profile])
             X_train = self.df[profile][['GSR']].values
             y_train_rf = self.df[profile]['Bullet Speed'].values
             self.rf_game[profile].fit(X_train, y_train_rf)
             score[profile] = str(round(self.rf_game[profile].score(X_test, y_test_rf),2)) # calculate accuracy bullet speed
             print("Accuracy bullet speed with random forests for profile #" + str(profile) + ": " + score[profile])
             
         self.best_profile_index = max(score, key=score.get)
         X_train = self.df[self.best_profile_index][['GSR']].values
         y_train_rf = self.df[self.best_profile_index]['Bullet Speed'].values
         print("The best profile is profile #" + str(self.best_profile_index) + " with accuracy of " + score[self.best_profile_index])
         self.rf_game.fit(X_train, y_train_rf)    # SAVE THIS
        
         # Linear Regression for stress levels and bullet speed when gsr outside profile range
         y_train_lr_exception = self.df[self.best_profile_index][['Bullet Speed']].values
         self.lr_game_exception.fit(X_train, y_train_lr_exception)
         
         # Linear Regression for HR
         y_train_lr = self.df[self.best_profile_index][['Heart Rate']].values
         self.lr_game.fit(X_train, y_train_lr)      # SAVE THIS
         
         # Inherit baseline heart rate of best profile
         print("The baseline heart rate is " + self.hr_rest[self.best_profile_index])
         
         

         
        
        