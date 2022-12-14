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
import other_files.game as main_game
import other_files.gui as gui
import other_files.calibration as calibration

ser = serial.Serial('COM3', 9600, timeout=0)
time.sleep(3)

# Note to Aleks: efficiently put in function arguments to call from the calibration.py file
# so right now, I just have them named as they were in the other file

class Outputs():
    def predict_stress(self,gui:gui.slider_value, calibration:calibration.rf_game.fit, calib:calibration.lr_game.fit):
        while True:
            try:
                bullet_speed = gui.slider_value*5
                ser_bytes = ser.readline()
                decoded_bytes = ser_bytes.decode("utf-8")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                
                if (decoded_bytes > max_gsr or decoded_bytes < min_gsr):
                    self.predicted_stress = calibration.lr_game_exception.fit.predict(decoded_bytes) # outputs speed
                else:
                    self.predicted_stress = calibration.rf_game.fit.predict(decoded_bytes)  # outputs speed
                    
                self.predicted_hr = calibration.lr_game.fit.predict(decoded_bytes)    # outputs heart rate
              
                # Save data for new profile (optional since no heart rate)
                # with open("Game_GSR.csv","a") as f:
                #     f.write(current_time +"," + bullet_speed + "," + decoded_bytes + "\n")
                #     time.sleep(0.01)           
            except:
                ser.close()
                print("Keyboard Interrupt")
                break
    
    # Converts outputted speed into values for outputs
    def outputs(self,calibration:calibration.rf_game.fit, calib:calibration.lr_game.fit):
        PWM = 0
        TENS = 0
        Volume = 0
    
        while True:
            if (self.predicted_stress < 0):
                PWM = 0
                TENS = 0
                Volume = 10
            elif (self.predicted_stress > 50):
                PWM = 255
                TENS = 1   
                Volume = 50
            else:
                PWM = (self.predicted_stress / 50) *255
                Volume = round(self.predicted_stress)
                if (self.predicted_stress > 30):
                    TENS = 1
                else:
                    TENS = 0 
