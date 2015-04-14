# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 00:33:10 2015

@author: tx
"""


from bs4 import BeautifulSoup


flabel = open(r'data\test.label.cn.txt')

souplabel = BeautifulSoup(flabel)
datalabel =[]
    
x = souplabel.review
    
for i in range(2500):
    z = x['label']
    datalabel.append(int(z))    
    x = x.find_next_sibling("review")

true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0
for i in range (2500):
    if datalabel[i] == relist[i] == 1:
        true_positive += 1
    if datalabel[i] == relist[i] == 0:
        true_negative += 1
    if datalabel[i] == 1 and relist[i] == 0:
        false_negative +=1
    if  datalabel[i] == 0 and  relist[i] == 1:
        false_positive +=1
         
print "TP:"+str(true_positive)
print "TN:"+str(true_negative)
print "FP:"+str(false_positive)
print "FN:"+str(false_negative)
precision = float(true_positive) / (true_positive + false_positive)
recall = float(true_positive) / (true_positive + false_negative)
f1 = 2 / (1 / precision + 1 / recall)
print "precision="+str(precision)
print "recall="+str(recall)
print "F1="+str(f1)


