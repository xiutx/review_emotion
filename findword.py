# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 15:07:10 2015

@author: tx
"""

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import itertools

from bs4 import BeautifulSoup
import sys
import csv
import jieba  
import time
import sys
import re
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
    
fp = open('data\cn_sample_data\sample.positive.txt')

soupp = BeautifulSoup(fp)
datap =[]
    
x = soupp.review
    
for i in range(4999):
    z = x.get_text(strip=True)
    z = review_to_wordlist(z)
    datap.append(z)    
    x = x.find_next_sibling("review")



fn = open('data\cn_sample_data\sample.negative.txt')
datan = []
soupn = BeautifulSoup(fn)
x = soupn.review    
for i in range(5000):
    z = x.get_text(strip=True)
    z = review_to_wordlist(z)
    datan.append(z)    
    x = x.find_next_sibling("review")


def create_word_scores():

    posWords = list(itertools.chain(*datap)) #把多维数组解链成一维数组
    negWords = list(itertools.chain(*datan)) #同理

    word_fd = nltk.FreqDist()
    cond_word_fd = ConditionalFreqDist() #可统计积极文本中的词频和消极文本中的词频
    for word in posWords:
        word_fd[word] += 1
        cond_word_fd['pos'][word] += 1
    for word in negWords:
        word_fd[word] += 1
        cond_word_fd['neg'][word] += 1

    pos_word_count = cond_word_fd['pos'].N() #积极词的数量
    neg_word_count = cond_word_fd['neg'].N() #消极词的数量
    total_word_count = pos_word_count + neg_word_count

    word_scores = {}
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count) #计算积极词的卡方统计量，这里也可以计算互信息等其它统计量
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count) #同理
        word_scores[word] = pos_score + neg_score #一个词的信息量等于积极卡方统计量加上消极卡方统计量

    return word_scores #包括了每个词和这个词的信息量

    


def find_best_words(word_scores, number):

    best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number] #把词按信息量倒序排序。number是特征的维度，是可以不断调整直至最优的
    best_words = set([w for w, s in best_vals])
    return best_words
    
word_scores = create_word_scores()



def best_word_features(words):
    return ([word for word in words if word in best_words])

def pos_features(feature_extraction_method):
    posFeatures = []
    for i in datap:
        posWords = feature_extraction_method(i) #为积极文本赋予"pos"
        posFeatures.append(" ".join(posWords))
    return posFeatures

def neg_features(feature_extraction_method):
    negFeatures = []
    for j in datan:
        negWords = feature_extraction_method(j) #为消极文本赋予"neg"
        negFeatures.append(" ".join(negWords))
    return negFeatures
    

ftest = open(r'data\test.cn.txt')

souptest = BeautifulSoup(ftest)
datatestone = []
    
x = souptest.review
    
for i in range(2500):
    z = x.get_text(strip=True)
    z = review_to_wordlist(z)
    datatestone.append(z)    
    x = x.find_next_sibling("review")
    
def test_features(feature_extraction_method):
    testFeatures = []
    for i in datatestone:
        testWords = feature_extraction_method(i)
        print testWords
        print i
        testFeatures.append(" ".join(testWords))
    return testFeatures





best_words = find_best_words(word_scores, 1500) #选择信息量最丰富的1500个的特征


posFeatures = pos_features(best_word_features)
negFeatures = neg_features(best_word_features)
testFeatures = test_features(best_word_features)
train = posFeatures+negFeatures


vectorizer=CountVectorizer()
train_data = vectorizer.fit_transform(train)
train_data = train_data.toarray()

test_data = vectorizer.transform(testFeatures)
test_data = test_data.toarray()

forest = MultinomialNB().fit( train_data, Y )

forest = LogisticRegression()

forest = forest.fit( train_data, Y )
result = forest.predict(test_data)
relalala=list(result)