import os
import sqlalchemy
import logging
import datetime
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
    if request.method == "GET":
        return get_movies(request)
    elif request.method == "POST":
        return save_movie()


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
    
def save_movie():
    global db
    ret = ""
    with db.connect() as conn, open("movies.sql", "r") as movies, open("ratings.sql", "r") as ratings:
        for movie in movies:
            conn.execute(movie)

        for rating in ratings:
            conn.execute(rating)

    return ret