#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 09:28:41 2025

@author: tze
"""

import os

dirname=os.path.dirname(os.path.abspath(__file__))
os.chdir(dirname)
os.system('git submodule update --init --recursive --remote')
for item in ['tkWindget', 'RW_data', 'AppHub', 'DataProcess', 'Figures']:
    if os.path.isdir(os.path.join(dirname,item)):
        os.chdir(os.path.join(dirname,item))
        os.system('git checkout main')
