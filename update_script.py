#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 09:28:41 2025

@author: tze
"""

import os

os.system('git pull origin main')
dirname=os.path.dirname(os.path.abspath(__file__))
for item in ['tkWindget', 'RW_data', 'AppHub', 'DataProcess', 'Figures']:
    if os.path.isdir(os.path.join(dirname,item)):
        os.chdir(os.path.join(dirname,item))
        os.system('git pull origin main')
