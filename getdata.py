"""
Created on Sat Apr 11 18:29:44 2015

@author: tx
"""
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys
import csv
import jieba  
import time
import sys
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

start_time = time.clock()
stopfile = open('data\stop.txt')
stopwords = stopfile.read().decode('utf-8').split('\n')

def bag_of_words(words):
    return dict([(word, True) for word in words])
    
def review_to_wordlist(review):
    words = jieba.cut(review)
    words = [w for w in words if not w in stopwords]
    return(words)
    
fp = open('data\cn_sample_data\sample.positive.txt')

soupp = BeautifulSoup(fp)
data =[]
    
x = soupp.review
    
for i in range(4999):
    z = x.get_text(strip=True)
    data.append(z)    
    x = x.find_next_sibling("review")


fn = open('data\cn_sample_data\sample.negative.txt')

soupn = BeautifulSoup(fn)
x = soupn.review    
for i in range(5000):
    z = x.get_text(strip=True)
    data.append(z)    
    x = x.find_next_sibling("review")
    

clean_train_reviews = []
for i in xrange( 0, len(data)):
        clean_train_reviews.append(" ".join(review_to_wordlist(data[i])))





Y = []

for i in range(9999):
    if i<5000:
        Y.append(1)
    else:
        Y.append(0)
vectorizer=CountVectorizer()
train_data_features = vectorizer.fit_transform(clean_train_reviews)
train_data_features = train_data_features.toarray()

forest = RandomForestClassifier(n_estimators = 100)
forest = forest.fit( train_data_features, Y )





ftest = open(r'data\test.cn.txt')

souptest = BeautifulSoup(ftest)
datatest =[]
    
x = souptest.review
    
for i in range(2500):
    z = x.get_text(strip=True)
    datatest.append(z)    
    x = x.find_next_sibling("review")

clean_test_reviews = []
for i in xrange( 0, len(datatest)):
        clean_test_reviews.append(" ".join(review_to_wordlist(datatest[i])))    
    
test_data_features = vectorizer.transform(clean_test_reviews)
test_data_features = test_data_features.toarray()

result = forest.predict(test_data_features)
relalala=list(result)


stop_time = time.clock()
print stop_time - start_time



