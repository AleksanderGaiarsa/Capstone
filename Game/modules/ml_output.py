# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 23:25:15 2022

@author: nguye
"""

import serial
import time
import csv
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import modules.gui as gui
import modules.calibration as calibration

# Note to Aleks: efficiently put in function arguments to call from the calibration.py file
# so right now, I just have them named as they were in the other file

#Designed with serial output 

class Outputs():
    def __init__(self):
        self.pwm = 125

    def predict_stress(self, gsr_val, calibration:calibration.Calibration):

        #predict stress

        if ((gsr_val > int(float(calibration.max_gsr))) or (gsr_val < int(float(calibration.min_gsr)))):
            self.predicted_stress = int(calibration.lr_game_exception.predict([[gsr_val]])[0]) # outputs speed
        else:
            self.predicted_stress = int(calibration.rf_game.predict([[gsr_val]])[0])  # outputs speed
            
        self.predicted_hr = round(calibration.lr_game.predict([[gsr_val]])[0][0],3)    # outputs heart rate


    # Converts outputted speed into values for outputs
    def outputs(self):
        if (self.predicted_stress < 0):
            self.pwm = 0
        elif (self.predicted_stress > 60):
            self.pwm = 255  
        else:
            self.pwm = (self.predicted_stress / 60) * 255
