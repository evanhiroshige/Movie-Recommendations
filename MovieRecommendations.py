import json
import numpy as np
import pandas
import time

"""
TODO
Implement genre filtered searches
searching for movie, if typo, suggests closest name e.g. enter movie: toy stroy - "Did you mean toy story"
make it faster (possibly with some stats)

"""


# converts raw movie csv data to dictionaries
def jsonify(movie_file, ratings_file):
    # movie_info: first column is movie id, second is movie title, third is genre
    movie_info = pandas.io.parsers.read_csv(movie_file, delimiter=',', dtype=None, encoding=None).values
    # ratings: first column is user id, second is movie id, third is rating
    ratings = pandas.io.parsers.read_csv(ratings_file, delimiter=',', dtype=None, encoding=None).values
    movie_dict = {}
    title_to_id = {}
    for i in range(0, len(movie_info)):
        title: str = movie_info[i][1]
        movie_id: int = movie_info[i][0]
        genres = movie_info[i][2]
        movie_dict[movie_id] = {"title": title, "genres": genres}
        title_to_id[title] = movie_id
    movie_dict["key"] = title_to_id

    with open('movies.json', 'w') as file:
        file.write(json.dumps(movie_dict))

    # ratings_dict = {}
    movie_id_to_critic_ratings = {}

    for i in range(0, len(ratings)):
        critic_id: int = ratings[i][0]
        movie_id: int = ratings[i][1]
        rating: float = ratings[i][2]

        #critic: dict = ratings_dict.get(critic_id, {})
        #critic[int(movie_id)] = rating
        #ratings_dict[int(critic_id)] = critic

        critic_to_rating: dict = movie_id_to_critic_ratings.get(movie_id, {})
        critic_to_rating[int(critic_id)] = rating
        movie_id_to_critic_ratings[int(movie_id)] = critic_to_rating

    # with open('ratings.json', 'w') as file:
    # file.write(json.dumps(ratings_dict))

    with open('movie_to_ratings.json', 'w') as file:
        file.write(json.dumps(movie_id_to_critic_ratings))


# converts json data to a dictionary
def djsonify(json_file):
    with open(json_file, 'r') as file:
        json_data = file.read()

    return json.loads(json_data)


# title: (str) name of movie
# movies: (dict) key: movie id, value: (dict) title and genre
# move_to_critic_ratings: (dict) key: movie id, value: (dict) key: critic id, value: rating
def get_recommendations(title, movies, movie_to_critic_rating):
    min_reviews = 20
    """
    :type title: str
    :type movies: dict
    :type critic_ratings: dict
    :type movie_to_critic_rating: dict
    """
    title_to_id: dict = movies["key"]
    movie_id = str(int(title_to_id.get(title, -1)))
    ratings_for_search = movie_to_critic_rating.get(movie_id, -1)
    if movie_id == -1:
        raise Exception(title + " could not be found in library.")
    if movie_id not in movie_to_critic_rating or len(ratings_for_search.items()) < min_reviews:
        raise Exception("Not enough reviews for " + title + " to recommend movies")

    recommendations = []
    # for each corresponding movie
    for movie_compare, ratings_compare in movie_to_critic_rating.items():
        if movie_compare == movie_id or len(ratings_compare.keys()) < min_reviews:
            continue
        distance = 0
        critic_count = 0
        for critic, rating in ratings_for_search.items():
            if critic in ratings_compare:
                critic_count += 1
                distance += ((ratings_for_search[critic] - ratings_compare[critic]) ** 2)
        if critic_count < min_reviews:
            continue
        average_distance = distance ** .5 / critic_count
        recommendations.append((average_distance, movies[movie_compare]["title"],
                                movies[movie_compare]["genres"]))
    recommendations = sorted(recommendations, key=lambda rec: rec[0])
    print("Title, Genre(s), Confidence")
    for pair in recommendations:
        print(pair[1] + ", ", pair[2] + ", ", pair[0])
    return recommendations


def main():
    # jsonify("big_movies.csv", "big_ratings.csv")
    movies = djsonify("movies.json")
    movie_to_critic_rating = djsonify("movie_to_big_ratings.json")
    title = input("Enter movie title: ")
    t = time.time()
    get_recommendations(title, movies, movie_to_critic_rating)
    print(time.time() - t)


main()
