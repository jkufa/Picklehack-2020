from flask import Flask, render_template, request, redirect
from twython import Twython
from model import *

app = Flask(__name__)
app.debug=True

keys = []
f = open("TWITTER_KEYS.txt", "r")
for line in f:
  keys.append(line.rstrip('\n').rsplit(': ', 1)[1])
twitter = Twython(keys[0], access_token=keys[2]) 
f.close()


@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "POST":
    req = request.form
    url = req.get('tweet-url').split('/')
    status_id = url[len(url)-1]
    data =  twitter.lookup_status(id=status_id)
    for tweet in data:
        unfiltered = tweet["text"]
    return redirect(request.url)
  return render_template('index.html')

if __name__ == '__main__':
  app.run()