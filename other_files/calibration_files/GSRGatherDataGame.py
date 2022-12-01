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


def predict_stress(gui:gui.slider_value, calibration:calibration.rf_game.fit):
    while True:
        try:
            bullet_speed = gui.slider_value*5
            ser_bytes = ser.readline()
            decoded_bytes = ser_bytes.decode("utf-8")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(decoded_bytes + "\n")
            predicted_stress = calibration.rf_game.fit.predict(decoded_bytes)
            print(predicted_stress)     # predicted stress level
            # Save data for new profile (optional since no heart rate)
            # with open("Game_GSR.csv","a") as f:
            #     f.write(current_time +"," + bullet_speed + "," + decoded_bytes + "\n")
            #     time.sleep(0.01)           
        except:
            ser.close()
            print("Keyboard Interrupt")
            break

# Add if time permits (Sunday)
#def outputs(calibration:calibration.lr_game.fit):
    
