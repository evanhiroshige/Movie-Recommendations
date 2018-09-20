import json
import numpy as np
import pandas

# converts raw movie data to dictionaries
def jsonify(movie_file, ratings_file):
    # movie_info: first column is movie id, second is movie title, third is genre
    movie_info = pandas.io.parsers.read_csv(movie_file, delimiter=',', dtype=None, encoding=None).values
    # ratings: first column is user id, second is movie id, third is rating
    ratings = pandas.io.parsers.read_csv(ratings_file, delimiter=',', dtype=None, encoding=None).values
    # userMovie = input("Enter a movie: ")
    movie_dict = {}
    for i in range(0, len(movie_info)):
        title: str = movie_info[i][1]
        movie_dict[movie_info[i][0]] = {"title": title[0: -7], "genres": movie_info[i][2]}

    with open('movies.json', 'w') as file:
        file.write(json.dumps(movie_dict))

    ratings_dict = {}

    for i in range(0, len(ratings)):
        critic = ratings_dict.get(ratings[i][0], {})
        critic[ratings[i][1]] = ratings[i][2]

# converts json data to a dictionary
def djsonify(json_file):
    with open('ratings.json', 'r') as file:
        json_data = file.read()

    return json.loads(json_data)
