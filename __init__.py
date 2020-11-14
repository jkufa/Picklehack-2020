from flask import Flask, render_template, request, redirect
from twython import Twython
import re
import sys, os

sys.path.insert(0, os.getcwd()+"/")
from model import DeepLearning

# from model import *

app = Flask(__name__)
app.debug=True
# dl = DeepLearn()

keys = []
f = open("TWITTER_KEYS.txt", "r")
for line in f:
  keys.append(line.rstrip('\n').rsplit(': ', 1)[1])
twitter = Twython(keys[0], access_token=keys[2]) 
f.close()

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

@app.route('/', methods=["GET", "POST"])
def index():
  button_pressed = False
  is_gamer = False
  url = ""
  f1_score = 0
  if request.method == "POST":
    req = request.form
    url = req.get('tweet-url').split('/')
    status_id = url[len(url)-1]
    data =  twitter.lookup_status(id=status_id, tweet_mode='extended')
    for tweet in data:
        unfiltered = tweet["full_text"]
    unfiltered = unfiltered.replace('\n', ' ')
    filtered = remove_garbage(unfiltered)
    dl = DeepLearning(filtered)
    # TODO: Run run tweet against model
    # print(filtered, dl.f1)
    # print(filtered, dl.f1)
    button_pressed = True
    # return redirect(request.url, button_pressed=button_pressed)
    return render_template('index.html',button_pressed=button_pressed,tweet_url=req.get('tweet-url'), is_gamer=False, f1_score=.32*100)
  return render_template('index.html',button_pressed=button_pressed)

@app.route('/check_tweet')
def check_tweet():
  return render_template('check_tweet.html')

if __name__ == '__main__':
  app.run()

def hack_bs(url_id):
  print("yo")