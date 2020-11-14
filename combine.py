import os

directory = 'data'

item_id = 0

w = open("raw.csv", "w")


for filename in os.listdir(directory):
  f = open(os.path.join(directory, filename), 'r')
  for i in f.readlines():
    item_id += 1

    extract = i.split(',',1)[1]
    new_prefix = str(item_id) + ','

    fixed = new_prefix + extract

    w.write(fixed)

f.close()
w.close()
