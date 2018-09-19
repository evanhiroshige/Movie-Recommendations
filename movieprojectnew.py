import numpy as np
m = np.genfromtxt('biggerdata.csv', delimiter=',', dtype=None)

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

print X
