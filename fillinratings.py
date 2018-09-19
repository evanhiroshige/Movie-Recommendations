import numpy as np
movienamekey = np.genfromtxt("NAMES.csv", delimiter="|", dtype=None)
m = np.genfromtxt('biggerdata.csv',delimiter=',',dtype=None)

n = len(m)
# finds total number of critics
T = np.max([int(e) for e in m[:, 1]])

# creates list of all the different movie ids
ids = []
for i in range(0, n-1):
    if m[i-1][0] != m[i][0]:
        ids.append(m[i][0])

# creates matrix of zeroes that will eventually turn into final matrix
counter = len(ids)
X = np.zeros((T * counter, 3))

# sets values in columns 1 and 2 to the correct values
for l in range(0, counter):
    g = 1
    for i in range(T * l, T * (l+1)):
        X[i][0] = ids[l]
        X[i][1] = g
        g += 1

q = len(X)
l = 0
for i in range(q):
    if l == n:
        break
    elif X[i][1] == m[l][1] and X[i][0] == m[l][0]:
        X[i][2] = m[l][2]
        l += 1

data = X
print X

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
    print "s"
    compare = []
    dif = []
    for l in range(ldata):
        if key[i] == data[l][0] and key[i] != movie:
            compare.append(data[l][2])
            if len(r) == len(compare):
                for k in range(len(r)):
                    dif.append((r[k]-compare[k]) ** 2)
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
for i in range(10):
        print movienamekey[last[i + 1]][1]
