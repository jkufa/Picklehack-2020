from twython import Twython
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
import warnings
import sys
import csv
import random
import string
import json

import nltk
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

stemmer = PorterStemmer()





class Row:

#id is PK, flag is "is gamer tweet", data is the tweet data
  def __init__(self, item_id, status, analyze):
    self.id = item_id
    
    self.flag = status

    #tokenize and stemming
    my_set = analyze.split()
    for i in range(len(my_set)):
      my_set[i] = stemmer.stem(my_set[i])

    final_data = ""
    for i in range(len(my_set)):
      final_data += my_set[i] + " "
    
    self.data = final_data

  def rtr_string(self):
    return (str(self.id) + ',' + self.flag + ',' + self.data + '\n')


f = open("raw.csv", "r")

w = open("training.csv", "w")
x = open("testing.csv", "w")

w.write('id,flag,data\n')
x.write('id,flag,data\n')

iterator = 0

for i in f.readlines():
  iterator += 1
  item_id = i.split(',')[0]
  flag = i.split(',')[1]
  data = i.split(',')[2]

  class_obj = Row(item_id, flag, data)

  if iterator % 2 == 0:
    x.write(class_obj.rtr_string())
  else:
    w.write(class_obj.rtr_string())


train = pd.read_csv('training.csv')
test = pd.read_csv('testing.csv')

combi = train.append(test, ignore_index=True)


bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')

bow = bow_vectorizer.fit_transform(combi['data'])

train_bow = bow[:31962, :]
test_bow = bow[31962:, :]

xtrain_bow, xvalid_bow, ytrain, yvalid = train_test_split(train_bow, combi['flag'], random_state=42, test_size=0.3)

lreg = LogisticRegression()
lreg.fit(xtrain_bow, ytrain)

prediction = lreg.predict_proba(xvalid_bow)
prediction_int = prediction[:,1] >= 0.3
prediction_int = prediction_int.astype(np.int)



#tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')

#tfidf = tfidf_vectorizer.fit_transform(combi['data'])








print(f1_score(yvalid, prediction_int))