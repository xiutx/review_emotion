"""
Created on Sat Apr 11 18:29:44 2015

@author: tx
"""
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import jieba  
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB 

start_time = time.clock()
stopfile = open('data\stop.txt')
stopwords = stopfile.read().decode('utf-8').split('\n')

def bag_of_words(words):
    return dict([(word, True) for word in words])

    
def review_to_wordlist(review):    
    words = jieba.cut(review)
    words = [w for w in words if not w in stopwords]
    return(words)


def get_data(flie,lcount,data):
    
    soupp = BeautifulSoup(flie)
    x = soupp.review
    
    for i in range(lcount):
        z = x.get_text(strip=True)
        data.append(z)    
        x = x.find_next_sibling("review")
    

def trans_train_data(data): 
    for i in xrange( 0, len(data)):
        clean_train_reviews.append(" ".join(review_to_wordlist(data[i])))
        
    train_data_features = vectorizer.fit_transform(clean_train_reviews)
    train_data_features = train_data_features.toarray()

    return train_data_features

def trans_test_data(datatest):
    clean_test_reviews = []
    for i in xrange( 0, len(datatest)):
        clean_test_reviews.append(" ".join(review_to_wordlist(datatest[i])))
            
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()
    
    return test_data_features


def get_Y():
    Y = []

    for i in range(9999):
        if i<5000:
            Y.append(1)
        else:
            Y.append(0)
    
    return Y


vectorizer=CountVectorizer()
data =[]
clean_train_reviews = []
fp = open('data\cn_sample_data\sample.positive.txt')
get_data(fp,4999,data)

fn = open('data\cn_sample_data\sample.negative.txt')
get_data(fn,5000,data)

train_data = trans_train_data(data)


datatest =[]
clean_test_reviews = []
ftest = open(r'data\test.cn.txt')
get_data(ftest,2500,datatest)

test_data = trans_test_data(datatest)


#forest = RandomForestClassifier(n_estimators = 100)
#forest = svm.SVC(kernel='linear',C=10)
#forest = LogisticRegression()  
forest = MultinomialNB().fit( train_data,  get_Y() )
#forest = forest.fit( train_data, get_Y() )
result = forest.predict(test_data)

relist=list(result)

stop_time = time.clock()
print stop_time - start_time



