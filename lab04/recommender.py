import pandas as pd
import numpy as np
import boto3
import simplejson as json

s3_client = boto3.resource("s3")

"""

dict form: {Hans-Peter: {Hans-Ueli: 0.5}, Hans-Ruedi: {Hans-Peter: 0.6}}
dict form: {Movie a: {Movie b: 0.5}, Movie b: {Movie c: 0.6}}
"""
# user_movie_watch_matrix, user_rating_matrix, users
def calculate_similarity_matrix(event, context):
    user_rating_matrix = event[0]["user_rating_matrix"]
    users = event[0]["users"]

    user_movie_watch_matrix = json.loads(s3_client.Object("movierecommenderdata", "data.json").get()["Body"].read())["user_movie_watch_matrix"]
    
    # Orig
    user_similarity_matrix = {}
    users = list(users)
    
    for user in users:
        user_similarity_matrix[user] = {}
        user_rating_magnitude = np.sqrt(sum(rating ** 2 for rating in user_rating_matrix[user].values()))
        
        for other_user in users:
            if user != other_user:
                other_user_rating_magnitude = np.sqrt(sum(rating ** 2 for rating in user_rating_matrix[other_user].values()))
                common_movies = user_movie_watch_matrix[user][other_user]
                user_ratings = [user_rating_matrix[user].get(movie) for movie in common_movies]
                other_user_ratings = [user_rating_matrix[other_user].get(movie) for movie in common_movies]
                similarity = np.dot(user_ratings, other_user_ratings) / (user_rating_magnitude * other_user_rating_magnitude)
                user_similarity_matrix[user][other_user] = similarity

    s3_client.Bucket("movierecommenderdata").put_object(Key="data2.json", Body=bytes(json.dumps(user_similarity_matrix).encode('UTF-8')))

    return {
        "user_rating_matrix": event[0]["user_rating_matrix"],
        "users": event[0]["users"],
        "movies": event[0]["movies"]
    }

"""

dict form: {Hans-Peter: {Hans-Ruedi: {common_movies: [1,2,3,4], uncommon_movies: [5,6]}}}
"""
# user_rating_matrix, movies, users, user_based = True
def compare_user_ratings(event, context):
    user_rating_matrix = event["user_rating_matrix"]
    users = set(event["users"])
    movies = set(event["movies"])
    user_based = True

    # Orig
    user_movie_watch_matrix = {}
    user_unwatched_movies_matrix = {}

    if user_based:
        users = list(users)
        for user in users:
            user_movie_watch_matrix[user] = {}
            user_unwatched_movies_matrix[user] = []
            for other_user in users:
                if user != other_user:
                    user_rated_movies = set(user_rating_matrix[user].keys())
                    other_user_rated_movies = set(user_rating_matrix[other_user].keys())
                    uncommon_movies = other_user_rated_movies.difference(user_rated_movies)
                    common_movies = user_rated_movies.intersection(other_user_rated_movies)
                    user_movie_watch_matrix[user][other_user] = list(common_movies)
                    user_unwatched_movies_matrix[user] += list(uncommon_movies)
                    
    else:
        movies = list(movies)
        for movie in movies:
            user_movie_watch_matrix[movie] = {}
            user_unwatched_movies_matrix[movie] = []
            for other_movie in movies:
                if movie != other_movie:
                    user_rated_movies = set(user_rating_matrix[movie].keys())
                    other_user_rated_movies = set(user_rating_matrix[other_movie].keys())
                    uncommon_movies = other_user_rated_movies.difference(user_rated_movies)
                    common_movies = user_rated_movies.intersection(other_user_rated_movies)
                    user_movie_watch_matrix[movie][other_movie] = list(common_movies)
                    user_unwatched_movies_matrix[movie] += list(uncommon_movies)

    user_ratings = {
        "user_movie_watch_matrix": user_movie_watch_matrix,
        "user_unwatched_movies_matrix": user_unwatched_movies_matrix
    }

    s3_client.Bucket("movierecommenderdata").put_object(Key="data.json", Body=bytes(json.dumps(user_ratings).encode('UTF-8')))

    return True

"""

dict form: {Hans-Ueli: {12345: 3}, Hans-Peter: {6789: 5}}
"""
#users, movies, df_uratings, user_based = True
def calculate_user_rating_matrix(event, context):
    users = set(event["users"])
    movies = set(event["movies"])
    df_uratings = pd.read_json(event["df_uratings"], orient="records")
    user_based = True

    # Orig
    user_rating_matrix = {}
    
    if user_based:
        for user in users:
            user_rating_matrix[user] = {}
            for movie in movies:
                movie_data = df_uratings[df_uratings["id"] == movie]
                if movie_data[movie_data["user"] == user]["rating"].size > 0:
                    rating = movie_data[movie_data["user"] == user]["rating"].iloc[0]
                    user_rating_matrix[user][movie] = rating

    else:
        for movie in movies:
            user_rating_matrix[movie] = {}
            for user in users:
                movie_data = df_uratings[df_uratings["id"] == movie]
                if movie_data[movie_data["user"] == user]["rating"].size > 0:
                    rating = movie_data[movie_data["user"] == user]["rating"].iloc[0]
                    user_rating_matrix[movie][user] = rating 

    return {
        "user_rating_matrix": user_rating_matrix,
        "users": event["users"],
        "movies": event["movies"],
        "df_movies": event["df_movies"]
    }

"""

dict form: {12345: [Hans-Ueli, Hans-Ruedi], 6789: [Hans-Peter, Lisa]}
"""
# movies, user_rating_matrix
def calculate_movie_rating_matrix(event, context):
    movies = event[0]["movies"]
    user_rating_matrix = event[0]["user_rating_matrix"]

    # Orig
    movie_rating_matrix = {}
    for movie in movies:
        movie_rating_matrix[movie] = []
        movie_int = movie
        for user in user_rating_matrix:
            movie = str(movie)

            if movie in list(user_rating_matrix[user].keys()):
                movie_rating_matrix[movie_int].append(user)

    return {
        "users": event[0]["users"],
        "movie_rating_matrix": movie_rating_matrix,
        "user_rating_matrix": event[0]["user_rating_matrix"]
    }

"""

dict form {56789: 3.5, 12345: 4.9}
"""
# user, movie_rating_matrix, user_similarity_matrix, user_rating_matrix, user_unwatched_movies_matrix, item_based_user_rating_matrix = None, user_based = True
def calculate_recommendation_matrix(event, context):
    client = boto3.resource("dynamodb")
    user_based = True
    user = json.loads(s3_client.Object("movierecommenderdata", "user.json").get()["Body"].read())
    movie_rating_matrix = event[1]["movie_rating_matrix"]
    user_similarity_matrix = json.loads(s3_client.Object("movierecommenderdata", "data2.json").get()["Body"].read())
    user_rating_matrix = event[0]["user_rating_matrix"]
    user_unwatched_movies_matrix = json.loads(s3_client.Object("movierecommenderdata", "data.json").get()["Body"].read())["user_unwatched_movies_matrix"]
    item_based_user_rating_matrix = None
    movie_table = client.Table("movies")
    df_movies = pd.read_json(json.dumps(movie_table.scan()["Items"]), orient="records")

    # Orig
    recommendations_matrix = {}
    if user_based:
        for uncommon_movie in user_unwatched_movies_matrix[user]:
            summe_zaehler = 0
            summe_nenner = 0
            for rated_by_user in movie_rating_matrix[uncommon_movie]:
                if rated_by_user != user:
                    summe_zaehler += user_similarity_matrix[user][rated_by_user] * user_rating_matrix[rated_by_user][uncommon_movie]
                    summe_nenner += user_similarity_matrix[user][rated_by_user]

            recommendations_matrix[uncommon_movie] = summe_zaehler / summe_nenner
    else:
        for unwatched_movie in user_unwatched_movies_matrix:
            if unwatched_movie in item_based_user_rating_matrix[user]:
                continue
            summe = 0
            coefficient_sum = 0
            for watched_movie, rating in item_based_user_rating_matrix[user].items():
                if rating != 0 and watched_movie != unwatched_movie:
                    summe += rating * user_similarity_matrix[watched_movie][unwatched_movie]
                    coefficient_sum += user_similarity_matrix[watched_movie][unwatched_movie]
            recommendations_matrix[unwatched_movie] = summe / coefficient_sum

    return map_movie_id_to_title(getRecommendations(recommendations_matrix), df_movies)

def getRecommendations(recommendation_matrix, top=3):
    sorted_recommendations = {}
    
    for recommendation_key in reversed(sorted(recommendation_matrix, key=recommendation_matrix.get)):
        sorted_recommendations[recommendation_key] = recommendation_matrix[recommendation_key]

    return list(sorted_recommendations)[:top]

def map_movie_id_to_title(ids, df_movies):
    titles = []
    for movie_id in ids:
        titles.append(df_movies[df_movies["id"] == int(movie_id)]["title"].iloc[0])
    return titles

def correct_wrong_user_data(user, movie_ratings_per_user, user_based = True):
    if user_based:
        for movie in movie_ratings_per_user[user]:
            if movie_ratings_per_user[user][movie] > 5.0 or movie_ratings_per_user[user][movie] < 0.0:
                movie_ratings_per_user[user][movie] = 0.0
            elif movie_ratings_per_user[user][movie] - int(movie_ratings_per_user[user][movie]) > 0:
                movie_ratings_per_user[user][movie] = round(movie_ratings_per_user[user][movie])
    else:
        for movie in movie_ratings_per_user:
            if user in movie_ratings_per_user[movie]:
                if movie_ratings_per_user[movie][user] > 5.0 or movie_ratings_per_user[movie][user] < 0.0:
                    movie_ratings_per_user[movie][user] = 0.0
                elif movie_ratings_per_user[movie][user] - int(movie_ratings_per_user[movie][user]) > 0:
                    movie_ratings_per_user[movie][user] = round(movie_ratings_per_user[movie][user])