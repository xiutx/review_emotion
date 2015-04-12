# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 00:33:10 2015

@author: tx
"""
import sys
import numpy as np
import pandas as pd
import time
import csv
from bs4 import BeautifulSoup


flabel = open(r'data\test.label.cn.txt')

souplabel = BeautifulSoup(flabel)
datalabel =[]
    
x = souplabel.review
    
for i in range(2500):
    z = x['label']
    datalabel.append(int(z))    
    x = x.find_next_sibling("review")

count = 0
for i in range (2500):
    if datalabel[i] == relalala[i]:
        count +=1

print count
