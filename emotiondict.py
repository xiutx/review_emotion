# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 00:30:48 2015

@author: tx
"""

filepdict = open(r'data\NTUSD_simplified\NTUSD_positive_simplified.txt')
datapset = set()
for line in filepdict:
    datapset.add(line.decode('utf-8'))


