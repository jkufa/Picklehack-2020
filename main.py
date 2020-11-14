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


tweet_id = 0

# "@[\w]*" for twitter handles 
# "[^a-zA-Z\s#]" for everything but letters and spaces
def remove_garbage(inpt):
  r = re.findall("@[\w]*", inpt)
  for i in r:
    inpt = re.sub(i, '', inpt)
  #remove links
  inpt = re.sub(r'http\S+', '', inpt)
  #remove special characters
  inpt = re.sub(r'[^a-zA-Z ]+', '', inpt)
  #remove words with 1-2 letters
  inpt = re.sub(r'\b\w{1,2}\b', '', inpt)
  return inpt

def random_date(d1, d2):
  start = datetime.strptime(d1, '%m/%d/%Y')
  end = datetime.strptime(d2, '%m/%d/%Y')

  delta = end - start
  int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
  random_second = randrange(int_delta)
  return start + timedelta(seconds=random_second)

def is_tweet_gamer(tweet):
  print(tweet)
  invalid_input = True
  while(invalid_input):
    is_gamer = input("Is the following tweet a gamer tweet? 2 = discard, 1 = yes, 0 = no: ")
    if(int(is_gamer) == 0 or int(is_gamer) == 1 or int(is_gamer) == 2):
      invalid_input = False
      print('\n')
      return int(is_gamer)
    else:
      print("Error: invalid input. Please try again.")

def get_tweets_username(twitter, username):
  data = twitter.get_user_timeline(screen_name=username, tweet_mode='extended', count=100)
  for tweet in data:
    if "retweeted_status" in tweet:
      unfiltered = tweet["retweeted_status"]["full_text"]
    else:
      unfiltered = tweet["full_text"]
    filtered = remove_garbage(unfiltered)
    label = is_tweet_gamer(unfiltered)
    if label != 2:
      # username is the filename
      csv_handling(username, label, filtered, unfiltered)    
  

def get_tweets_random(twitter):
  char = random.choice(string.ascii_letters)
  rand_time = random_date("1/1/2017", "11/13/2020")
  data = twitter.search(q=char, tweet_mode='extended', count=500, lang='en', result_type='mixed', since=rand_time)
  for tweet in data['statuses']:
    if random.randint(0,4) == 0:
      if "retweeted_status" in tweet:
        unfiltered = tweet["retweeted_status"]["full_text"]
        unfiltered = unfiltered.replace('\n', ' ')
      else:
        unfiltered = tweet["full_text"]
      filtered = remove_garbage(unfiltered)
      label = is_tweet_gamer(unfiltered)
      if label != 2:
        csv_handling("random", label, filtered, unfiltered)    

def csv_handling(filename, label, filt, unfilt):
  global tweet_id
  tweet_id += 1
  row = str(tweet_id) + ',' + str(label) + ',' + filt + ' \n'
  f = open('./data/'+filename+'.csv', 'a')
  f.write(row)
  f.close()

def main():
  keys = []
  f = open("TWITTER_KEYS.txt", "r")
  for line in f:
    keys.append(line.rstrip('\n').rsplit(': ', 1)[1])
  twitter = Twython(keys[0], access_token=keys[2]) 
  f.close()

  # Check arguments
  if len(sys.argv) > 1:
    username = sys.argv[1]
    f = open(username+'.csv', 'a')
    # TODO: Verify username exists
    get_tweets_username(twitter, username)
  else:
    try:
      f = open('./data/random.csv', 'r+')
      last_line = f.readlines()[-1]
      global tweet_id
      tweet_id = int(last_line.split(',')[0])
    except:
      f = open('./data/random.csv', 'a')
    get_tweets_random(twitter)
  f.close()


main()

