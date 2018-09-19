import numpy as np

movienamekey = np.genfromtxt('movienamekey.csv', delimiter=',', dtype=None)
data = np.genfromtxt('updatedmoviedata.csv', delimiter=',', dtype=None)

# TODO
# 1. Parse data to be much smaller
# 2. Figure out what this does
# 3. Rewrite faster
#
# Notes
#


movienums = len(movienamekey)
ldata = len(data)
movie = 0

# Takes movie name input
moviename = raw_input("Enter movie name: ")
for i in range(len(movienamekey)):
  if moviename == movienamekey[i][1]:
    movie = movienamekey[i][0]

# list of ratings
r = []
for i in range(ldata):
  if data[i][0] == movie:
    r.append(data[i][2])

# movie number key in array
key = []
for i in range(movienums):
  key.append(movienamekey[i][0])

# calculates distances
q = len(key)
distances = []
for i in range(q):
  compare = []
  dif = []
  for l in range(ldata):
    if key[i] == data[l][0] and key[i] != movie:
      compare.append(data[l][2])
      if len(r) == len(compare):
        for k in range(len(r)):
          dif.append((r[k] - compare[k]) ** 2)
        distances.append(sum(dif) ** 0.5)

# inserts zero into distances
zero = key.index(movie)
distances.insert(zero, 0)

# creates array with number of movies
last = []
for i in range(movienums):
  last.append(i)

# sorts distances and last in same way
distances, last = zip(*sorted(zip(distances, last)))

# prints rankings
for i in range(movienums - 1):
  print(movienamekey[last[i + 1]][1])
