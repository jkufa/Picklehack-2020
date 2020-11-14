from twython import Twython

keys = []
f = open("TWITTER_KEYS.txt", "r")
for line in f:
  keys.append(line.rstrip('\n').rsplit(': ', 1)[1])

twitter = Twython(keys[0], access_token=keys[2])


