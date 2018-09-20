import numpy as np

# movie id, title
movieInfo = np.genfromtxt('movienamekey.csv', delimiter=',', encoding=None, dtype=None)
# movie id, critic, rating
ratings = np.genfromtxt('updatedmoviedata.csv', delimiter=',', encoding=None, dtype=None)

# TODO
# 1. Parse data to be much smaller
# 2. Figure out what this does
# 3. Rewrite faster
#
# Notes
#


movie = -1

# FIND ID OF ENTERED MOVIE
# Takes movie name input
movieName = input("Enter movie name: ")
for i in range(len(movieInfo)):
    if movieName == movieInfo[i][1]:
        movie = movieInfo[i][0]
if (movie == -1):
    raise Exception("movie name not found")


# ADD ALL RATINGS OF MOVIE TO R
# list of ratings
r = []
for i in range(len(ratings)):
    if ratings[i][0] == movie:
        r.append(ratings[i][2])

# ADD ALL MOVIE IDS INTO AN ARRAY KEY
# movie number key in array
movieIds = []
for i in range(len(movieInfo)):
    movieIds.append(movieInfo[i][0])

# calculates distances
q = len(movieIds)
distances = []
for i in range(q):
    compare = []
    dif = []
    for l in range(len(ratings)):

        if movieIds[i] == ratings[l][0] and movieIds[i] != movie:
            compare.append(ratings[l][2])
            if len(r) == len(compare):
                for k in range(len(r)):
                    dif.append((r[k] - compare[k]) ** 2)
                distances.append(sum(dif) ** 0.5)
# inserts zero into distances
zero = movieIds.index(movie)
distances.insert(zero, 0)

# creates array with number of movies
last = []
for i in range(len(movieInfo)):
    last.append(i)

print(distances, last)

# sorts distances and last in same way
distances, last = zip(*sorted(zip(distances, last)))

# prints rankings
for i in range(len(movieInfo) - 1):
    print(movieInfo[last[i + 1]][1])
