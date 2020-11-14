import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
# import nltk
import warnings
# nltk.download('punkt')
# from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score


def DeepLearning(tweet):
  train = pd.read_csv('training.csv')
  test = pd.read_csv('testing.csv')

  combi = train.append(test, ignore_index=True)


  bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')

  bow = bow_vectorizer.fit_transform(combi['data'])
  tweet_arr = {tweet}
  # tweet_bow = bow_vectorizer.fit_transform(tweet_arr)

  train_bow = bow[:31962, :]
  test_bow = bow[31962:, :]

  xtrain_bow, xvalid_bow, ytrain, yvalid = train_test_split(train_bow, combi['flag'], random_state=42, test_size=0.3)

  lreg = LogisticRegression()
  lreg.fit(xtrain_bow, ytrain)

  # prediction = lreg.predict_proba(tweet_bow)
  prediction = lreg.predict_proba(xvalid_bow)
  prediction_int = prediction[:,1] >= 0.3
  prediction_int = prediction_int.astype(np.int)

  f1 = f1_score(yvalid, prediction_int)

# dl = DeepLearning("test")
