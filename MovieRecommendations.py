import time
from Serializers import djsonify

movie_file = "big_movies.json"
ratings_file = "movie_to_big_ratings.json"

min_reviews = 20
minimum_distance_factor = .5
movies = djsonify(movie_file)
movie_to_critic_rating = djsonify(ratings_file)

# title: (str) name of movie
# movies: (dict) key: movie id, value: (dict) title and genre
# move_to_critic_ratings: (dict) key: movie id, value: (dict) key: critic id, value: rating
def get_recommendations(title, genre=""):
    """
    :param genre: genre to filter by NOTE: should change this to a list in future
    :type title: str
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
        if movie_compare == movie_id or genre.lower() not in movies[movie_compare]["genres"].lower() or len(
                ratings_compare.keys()) < min_reviews:
            continue
        try:
            average_distance = compute_distance(ratings_for_search, ratings_compare)
        except:
            continue
        recommendations.append((average_distance, movies[movie_compare]["title"],
                                movies[movie_compare]["genres"]))
    recommendations = sorted(recommendations, key=lambda rec: rec[0])
    return recommendations


def compute_distance(ratings_for_search, ratings_compare):
    distance = 0
    critic_count = 0
    for critic, rating in ratings_for_search.items():
        if critic in ratings_compare:
            critic_count += 1
            distance += ((ratings_for_search[critic] - ratings_compare[critic]) ** 2)
    if critic_count < min_reviews:
        raise Exception()
    average_distance = (distance ** 0.5) / critic_count
    if (distance ** 0.5) / critic_count > minimum_distance_factor:
        raise Exception()
    return average_distance

def main():
    while True:
        title = input("Enter movie title: ")
        genre = input("Enter genre: ")
        try:
            t = time.time()
            rec = get_recommendations(title, genre)
            elapsed = time.time() - t
            print("Found", len(rec), "suggestions in %.3f" % elapsed, "seconds.")
            print("Title, Genre(s), Confidence\n")
            for pair in rec:
                print(pair[1] + ",", pair[2] + ", %.3f" % pair[0])
        except Exception as err:
            print(err)

main()