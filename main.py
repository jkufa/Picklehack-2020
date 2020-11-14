from twython import Twython
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
import warnings

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



keys = []
f = open("TWITTER_KEYS.txt", "r")
for line in f:
  keys.append(line.rstrip('\n').rsplit(': ', 1)[1])

twitter = Twython(keys[0], access_token=keys[2])

info = twitter.search(q='pog', tweet_mode='extended', count=200)

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(info)

for tweet in info['statuses']:
  print("Begin Tweet: ", end='')
  if "retweeted_status" in tweet:
    unfiltered = tweet["retweeted_status"]["full_text"]
    filtered = remove_garbage(unfiltered)
  else:
    unfiltered = tweet["full_text"]
    filtered = remove_garbage(unfiltered)
    print(unfiltered)
    print(filtered)


#t = open("new.txt", "w")
#for tweet in user_tweets:
 # t.write( str(tweet) + '\n' )

#t.close()