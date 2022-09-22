#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:15:59 2022

@author: aleksandergaiarsa
"""

#accelerometer data
atot_index = 0
counter_1=1

with open('acc_data.txt') as acc_data:
    line_count = 0
    atot = []
    for row in acc_data:
        column = row.split()
        if not row.startswith('#'):
            atot.append(column[4])
        if counter_1> 4504:
            break
        counter_1+=1
    atot.remove('atotal')
    n_atot = len(atot)