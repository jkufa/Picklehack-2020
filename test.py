from twython import Twython
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import string
# import nltk
import warnings
import sys
import csv
import random
import string
from random import randrange
from datetime import timedelta
from datetime import datetime



keys = []
f = open("TWITTER_KEYS.txt", "r")
for line in f:
  keys.append(line.rstrip('\n').rsplit(': ', 1)[1])
twitter = Twython(keys[0], access_token=keys[2]) 
f.close()


def random_date(start, end):

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


d1 = datetime.strptime("1/1/2017", '%m/%d/%Y')
d2 = datetime.strptime("1/1/2020", '%m/%d/%Y')

s = random_date(d1,d2)

data = twitter.search(q="a", tweet_mode='extended', count=500, lang='en', result_type='mixed', since=s)

for tweet in data['statuses']:
  if "retweeted_status" in tweet:
    print(tweet["retweeted_status"]["full_text"])
  else:
    print(tweet['full_text'])
