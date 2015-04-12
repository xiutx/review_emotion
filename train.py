# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:25:23 2015

@author: tx
"""
import sys
import numpy as np
import pandas as pd
import time
import csv
from bs4 import BeautifulSoup
import jieba  

start_time = time.clock()
print start_time
stopwords = list({}.fromkeys([line.rstrip() for line in open('data\stop.txt')]))
def review_to_wordlist(review):
    words = list(jieba.cut(review))   
    words = [w for w in words if not w in stopwords]
    return(words)
    
def gettrain():
    fp = open('data\cn_sample_data\sample.positive.txt')
    fn = open('data\cn_sample_data\sample.negative.txt')
    soupp = BeautifulSoup(fp)
    soupn = BeautifulSoup(fn)
    data_p = (soupp.get_text())
    data_n = (soupn.get_text()).split('\n\n')
    data = []
    
    pfile=file('data/pfile.csv', 'wb') 
    writer = csv.writer(pfile)

    
    for x in data_p:
        if  len(x) != x.count('\n'):
           data.append(review_to_wordlist(x))

    
gettrain()

stop_time = time.clock()
print stop_time - start_time
