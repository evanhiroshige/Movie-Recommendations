import json
import pandas


# converts raw movie csv data to json
def jsonify(movie_csv, movie_json_file_name, ratings_csv, ratings_json_file_name):
    # movie_info: first column is movie id, second is movie title, third is genre
    movie_info = pandas.io.parsers.read_csv(movie_csv, delimiter=',', dtype=None, encoding=None).values
    # ratings: first column is user id, second is movie id, third is rating
    ratings = pandas.io.parsers.read_csv(ratings_csv, delimiter=',', dtype=None, encoding=None).values

    movie_dict = {}
    title_to_id = {}
    for i in range(0, len(movie_info)):
        title: str = movie_info[i][1]
        movie_id: int = movie_info[i][0]
        genres = movie_info[i][2]
        movie_dict[movie_id] = {"title": title, "genres": genres}
        title_to_id[title] = movie_id
    movie_dict["key"] = title_to_id
    with open(movie_json_file_name, 'w') as file:
        file.write(json.dumps(movie_dict))

    movie_id_to_critic_ratings = {}
    for i in range(0, len(ratings)):
        critic_id: int = ratings[i][0]
        movie_id: int = ratings[i][1]
        rating: float = ratings[i][2]
        critic_to_rating: dict = movie_id_to_critic_ratings.get(movie_id, {})
        critic_to_rating[int(critic_id)] = rating
        movie_id_to_critic_ratings[int(movie_id)] = critic_to_rating
    with open(ratings_json_file_name, 'w') as file:
        file.write(json.dumps(movie_id_to_critic_ratings))


# converts json data to a dictionary
def djsonify(json_file):
    with open(json_file, 'r') as file:
        json_data = file.read()

    return json.loads(json_data)

