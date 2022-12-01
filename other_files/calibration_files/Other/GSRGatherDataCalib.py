# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 14:57:27 2022

@author: nguye
"""
import serial
import time
import csv
from datetime import datetime

# Put bullet speed here for now
bullet_speed = "10"

ser = serial.Serial('COM3', 9600, timeout=0)
time.sleep(3)

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode("utf-8")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time +"," + bullet_speed + "," + decoded_bytes + "\n")
        with open("Data3.csv","a") as f:
            f.write(current_time +"," + bullet_speed + "," + decoded_bytes + "\n")
            time.sleep(0.01)
    except:
        ser.close()
        print("Keyboard Interrupt")
        break