#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:15:59 2022

@author: aleksandergaiarsa
"""
import random

class Calibration():
    def __init__(self):
        #Base Readings
        self.base_heart = 0
        self.base_temp = 0

        for t in range(30):
            self.base_heart = self.base_heart + random.randrange(50,110,1)
            self.base_temp = self.base_temp + random.randrange(33,37,1)

        self.base_heart = round(self.base_heart/30,2)    # average
        self.base_temp = round(self.base_temp/30,2)
        self.current_heart = self.base_heart
        self.current_temp = self.base_temp
        self.step_heart = 80/self.base_heart
        self.step_temp = 500/self.base_temp
        self.prev_heart_ratio = 0
        self.heart_ratio = 0
        self.prev_temp_ratio = 0
        self.temp_ratio = 0