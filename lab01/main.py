import os
import sqlalchemy
import logging
import datetime
from recommender import *
import pandas as pd
from flask import jsonify

logger = logging.getLogger()

def init_db_connection():
    db_user = os.environ.get("DB_USER", "scad")
    db_pass = os.environ.get("DB_PASS", "scad")
    db_name = os.environ.get("DB_NAME", "scad")
    db_host = os.environ.get("DB_HOST", "localhost:3306")

    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    logger.info("Starting setup DB")
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_hostname,
            port=db_port,
            database=db_name,
        )
    )

    with pool.connect() as conn:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute(
            "CREATE TABLE movies "
            "( id int NOT NULL, title varchar(255) NOT NULL, "
            "languages varchar(255) NOT NULL, "
            "genres varchar(255) NOT NULL, "
            "rating numeric(3,1) NOT NULL, "
            "director varchar (255) NOT NULL, "
            "plot text NOT NULL, "
            "PRIMARY KEY (id) );"
        )

        conn.execute("DROP TABLE IF EXISTS ratings;")
        conn.execute(
            """
            CREATE TABLE ratings(
            id     INTEGER  NOT NULL
            ,user   VARCHAR(9) NOT NULL
            ,rating NUMERIC(4,1) NOT NULL
            );
            """
        )

    return pool
    
db = init_db_connection()

### Logic

def entrypoint(request):
    if request.path == "/recommend" and request.method == "GET":
        return create_recommendation()

    elif request.method == "POST":
        return save_movie()
    
    elif request.method == "GET":
        print(request.path)
        return get_movies(request)

def get_movies(request):
    global db
    ret = []
    with db.connect() as conn:
        for row in conn.execute(f"SELECT * from movies").fetchall():
            ret.append({
                "id": row["id"],
                "languages": row["languages"],
                "genres": row["genres"],
                "rating": float(row["rating"]),
                "director": row["director"],
                "plot": row["plot"]
            })
    return jsonify(ret)

def create_recommendation():
    recommendations = []
    with db.connect() as conn:
        df_uratings = pd.read_sql("SELECT * from ratings", conn)
        df_movies = pd.read_sql("SELECT * from movies", conn)

        users = set(df_uratings["user"])
        movies = set(df_uratings["id"])

        # User based
        user_rating_matrix = calculate_user_rating_matrix(users, movies, df_uratings)
        # Item based
        #item_based_user_rating_matrix = calculate_user_rating_matrix(users, movies, df_uratings, False)

        for user in users:
            #User based
            correct_wrong_user_data(user, user_rating_matrix)
            #Item based
            #correct_wrong_user_data(user, item_based_user_rating_matrix, False)

        # User based
        user_movie_watch_matrix, user_unwatched_movies_matrix = compare_user_ratings(user_rating_matrix, movies, users)
        similarity_matrix = calculate_similarity_matrix(user_movie_watch_matrix, user_rating_matrix, users)
        movie_rating_matrix = calculate_movie_rating_matrix(movies, user_rating_matrix)
        # Item based
        #item_based_user_movie_watch_matrix, item_based_user_unwatched_movies_matrix = compare_user_ratings(item_based_user_rating_matrix, movies, users, False)
        #item_based_similarity_matrix = calculate_similarity_matrix(item_based_user_movie_watch_matrix, item_based_user_rating_matrix, movies)
        #item_based_movie_rating_matrix = calculate_movie_rating_matrix(users, item_based_user_rating_matrix)
        
        for user in users:
            recommendation_matrix = calculate_recommendation_matrix(user, movie_rating_matrix, similarity_matrix, user_rating_matrix, user_unwatched_movies_matrix)
            #item_based_recommendation_matrix = calculate_recommendation_matrix(user, item_based_movie_rating_matrix, item_based_similarity_matrix, item_based_user_rating_matrix, #item_based_user_unwatched_movies_matrix, user_rating_matrix, False)
            #print('The user-based recommendations for ' + user + ' are: ' + str(map_movie_id_to_title(getRecommendations(recommendation_matrix), df_movies)))
            #print('The item-based recommendations for ' + user + ' are: ' + str(map_movie_id_to_title(getRecommendations(item_based_recommendation_matrix), df_movies)))

            recommendations.append(
                {
                    "user": user,
                    "movies": map_movie_id_to_title(getRecommendations(recommendation_matrix), df_movies)
                }
            )

    return jsonify(recommendations)

    
def save_movie():
    global db
    ret = ""
    with db.connect() as conn, open("movies.sql", "r") as movies, open("ratings.sql", "r") as ratings:
        for movie in movies:
            conn.execute(movie)

        for rating in ratings:
            conn.execute(rating)

    return ret