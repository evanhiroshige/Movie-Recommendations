import time
from Serializers import djsonify
import math


# title: (str) name of movie
# movies: (dict) key: movie id, value: (dict) title and genre
# move_to_critic_ratings: (dict) key: movie id, value: (dict) key: critic id, value: rating
def get_recommendations(title, movies, movie_to_critic_rating, genre=""):
    """
    :type title: str
    :type movies: dict
    :type critic_ratings: dict
    :type movie_to_critic_rating: dict
    """

    min_reviews = 20
    minimum_distance_factor = 1.25

    title_to_id: dict = movies["key"]
    movie_id = str(int(title_to_id.get(title, -1)))
    ratings_for_search = movie_to_critic_rating.get(movie_id, -1)
    if movie_id == -1:
        raise Exception(title + " could not be found in library.")
    if movie_id not in movie_to_critic_rating or len(ratings_for_search.keys()) < min_reviews:
        raise Exception("Not enough reviews for " + title + " to recommend movies")

    recommendations = []
    for movie_compare, ratings_compare in movie_to_critic_rating.items():
        close_enough = True
        if movie_compare == movie_id or genre.lower() not in movies[movie_compare]["genres"].lower() or len(ratings_compare.keys()) < min_reviews:
            continue
        distance = 0
        critic_count = 0
        for critic, rating in ratings_for_search.items():
            if critic in ratings_compare:
                critic_count += 1
                distance += ((ratings_for_search[critic] - ratings_compare[critic]) ** 2)
                if distance / critic_count > minimum_distance_factor:
                    close_enough = False
                    break
        if critic_count < min_reviews or not close_enough:
            continue
        average_distance = distance / critic_count  # (1/critic_count)
        recommendations.append((average_distance, movies[movie_compare]["title"],
                                movies[movie_compare]["genres"]))
    recommendations = sorted(recommendations, key=lambda rec: rec[0])
    return recommendations


movie_file = "big_movies.json"
ratings_file = "movie_to_big_ratings.json"


def main():
    movies = djsonify(movie_file)
    movie_to_critic_rating = djsonify(ratings_file)
    while True:
        title = input("Enter movie title: ")
        genre = input("Enter genre: " )
        try:
            t = time.time()
            rec = get_recommendations(title, movies, movie_to_critic_rating, genre)
            elapsed = time.time() - t
            print("Found ", len(rec), " suggestions in ", elapsed, " seconds.")
            print("Title, Genre(s), Confidence\n")
            for pair in rec:
                print(pair[1] + ", ", pair[2] + ", ", pair[0])
        except Exception:
            continue


main()
