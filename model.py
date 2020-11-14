import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import nltk
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# %matplotlib inline

# CHANGE THIS
train = pd.read_csv('~/Octokitty/Personal/Picklehack-2020/proof_of_concept/data/train.csv')
test = pd.read_csv('~/Octokitty/Personal/Picklehack-2020/proof_of_concept/data/test.csv')

# Removing Twitter handles

combi = train.append(test, ignore_index=True)

def remove_pattern(input_txt, pattern):
  r = re.findall(pattern, input_txt)
  for i in r:
    input_txt = re.sub(i, '', input_txt)

  return input_txt

combi['tidy_tweet'] = np.vectorize(remove_pattern)(combi['tweet'], "@[\w]*")
# Remove special characters, numbers, punctuation
combi['tidy_tweet'] = combi['tidy_tweet'].str.replace("[^a-zA-Z#]", " " )
# Removing short words
combi['tidy_tweet'] = combi['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))

tokenized_tweet = combi['tidy_tweet'].apply(lambda x: x.split())

from nltk.stem.porter import *
stemmer = PorterStemmer()

tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])

for i in range(len(tokenized_tweet)):
  tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

combi['tidy_tweet'] = tokenized_tweet

def hashtag_extract(x):
  hashtags = []
  for i in x:
    ht = re.findall(r"#(\w+)", i)
    hashtags.append(ht)
  return hashtags

HT_regular = hashtag_extract(combi['tidy_tweet'][combi['label'] == 0])
HT_negative = hashtag_extract(combi['tidy_tweet'][combi['label'] == 1])

HT_regular = sum(HT_regular, [])
HT_negative = sum(HT_negative, [])

# Bag of words model
from sklearn.feature_extraction.text import CountVectorizer
bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')

bow = bow_vectorizer.fit_transform(combi['tidy_tweet'])

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

# TODO: Change # of rows
train_bow = bow[:31962, :]
test_bow = bow[31962:, :]

xtrain_bow, xvalid_bow, ytrain, yvalid = train_test_split(train_bow, train['label'], random_state=42, test_size=0.3)

# Logistic Regression, fit data
lreg = LogisticRegression()
lreg.fit(xtrain_bow, ytrain) 

LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='warn', n_jobs=None, penalty='l2',
                   random_state=None, solver='warn', tol=0.0001, verbose=0,
                   warm_start=False)

prediction = lreg.predict_proba(xvalid_bow) # input
prediction_int = prediction[:,1] >= 0.3
prediction_int = prediction_int.astype(np.int) # Classifications
print(prediction_int)

f1_score(yvalid, prediction_int)